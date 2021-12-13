import json
import subprocess
import requests
import os
import math

container_list = subprocess.run(["docker ps -q --no-trunc"],capture_output=True, text=True,shell=True).stdout.splitlines()

cpus=8
default_quota = (int) (100000*cpus / len(container_list))

alpha_throt = 0.9
alpha_util = 0.2
target_throttle_time = 0
quota_step = 0.1
error_threshold = 1000
utilization_change_threshold = 0.05
default_weighted_error_parameter = 1

quota_upper_limit = cpus*100000
quota_lower_limit = 5000

def parse_partitions():
    f = open('partitions.json', 'r')
    partitions = json.load(f)
    return partitions

partitions = parse_partitions()

class container:
    def __init__(self, id, belongs):
        self.belongs = belongs
        self.partitions = []
        self.id = id
        self.cpu_quota = default_quota
        subprocess.run([f"docker update --cpu-quota={self.cpu_quota} {self.id}"],shell=True)

        util_file = "/sys/fs/cgroup/cpu/docker/"+self.id+"/cpuacct.usage"
        cur_utilization=""
        with open(util_file, 'r') as f:
            cur_utilization = (float)(f.readlines()[0])
        
        file_name = "/sys/fs/cgroup/cpu/docker/"+self.id+"/cpu.stat"
        CPU_stats=""
        with open(file_name, 'r') as f:
            CPU_stats = f.readlines()[2]
        cur_throttle_time = (float)(CPU_stats.split()[1])
        
        self.prev_throttle_time = cur_throttle_time
        self.prev_utilization = cur_utilization
    
    def utilization(self):
        util_file = "/sys/fs/cgroup/cpu/docker/"+self.id+"/cpuacct.usage"
        cur_utilization=""
        with open(util_file, 'r') as f:
            cur_utilization = float(f.readlines()[0])
            print("Util",cur_utilization)

        # alpha filter
        cur_utilization = alpha_util*cur_utilization + (1-alpha_util)*self.prev_utilization

        prev_utilization = self.prev_utilization
        self.prev_utilization = cur_utilization
        return cur_utilization-prev_utilization

    def throttle_time(self):
        file_name = "/sys/fs/cgroup/cpu/docker/"+self.id+"/cpu.stat"
        CPU_stats=""
        with open(file_name, 'r') as f:
            CPU_stats = f.readlines()[2]
        cur_throttle_time = (int)(CPU_stats.split()[1])
        
        # alpha filter
        cur_throttle_time = alpha_throt*cur_throttle_time + (1-alpha_throt)*self.prev_throttle_time
        
        prev_throttle = self.prev_throttle_time
        self.prev_throttle_time = cur_throttle_time
        return cur_throttle_time-prev_throttle

def create_ID_map():
    ID_map = {}
    for partition, container_ids in partitions.items():
        for c in container_ids:
            if c in ID_map:
                ID_map[c].partitions.append(partition)
            else:
                temp = container(c,1)
                ID_map[c] = temp
                ID_map[c].partitions.append(partition)
    
    # handle containers not in partition
    for c in container_list:
        if c not in ID_map:
            temp = container(c,0)
            ID_map[c] = temp
    
    return ID_map

ID_map = create_ID_map()

def init_prev_partiton_request():
    call_count = requests.get("http://localhost:16686/api/dependencies").json()
    partition_request = {}
    for item in call_count["data"]:
        if item["parent"] == "nginx-web-server":
            partition_request[item["child"]] = item["callCount"]
    return partition_request

prev_partition_request = init_prev_partiton_request()

def parse_weighted_error_parameters():
    global prev_partition_request
    call_count = requests.get("http://localhost:16686/api/dependencies").json()
    partition_request = dict()
    for item in call_count["data"]:
        if item["parent"] == "nginx-web-server":
            partition_request[item["child"]] = item["callCount"] - prev_partition_request[item["child"]]
    #print(partition_request)
    P = {}
    #something fishy here
    avg = sum(partition_request.values())/len(partition_request)
    #print(avg)
    if avg != 0 :
        for partition,req in partition_request.items():
            P[partition] = req/avg
    
    prev_partition_request = partition_request

    return P

# assuming no overlaps for now
def error_value():
    error_value={}
    print("error value start")

    # equation 1 in paper. Finds the error in throttle time, and 
    for _, containers in partitions.items():
        error = 0
        for container in containers:
            error += max((ID_map[container].throttle_time()-target_throttle_time),0)
        # deals with situations where containers overlap
        for container in containers:
            if container in error_value:
                error_value[container] = max(error,error_value[container])
            else:
                error_value[container] = error

    # deals with containers not in partitions
    for c in container_list:
        if ID_map[c].belongs == 0:
            error_value[c] = max((ID_map[container].throttle_time()-target_throttle_time),0)
    print("error value done")

    return error_value

def weighted_error_values():
    print("weighted error start")
    error_values = error_value()
    P = parse_weighted_error_parameters()
    #(error_values)
    weighted_error_values = {}
    #print(ID_map)
    if P:
        for container, value in error_values.items():
            # picks the max partition wise weight for the container if it's a part of a partition,
            # otherwise assignes the default weighted error partition, can look into this a bit more
            #print("***")
            # for k,v in ID_map.items():
            #     print(v.id, v.partitions, v.belongs)
            max_list = []
            if ID_map[container].belongs == 0:
                max_list.append(default_weighted_error_parameter)
            else:
                for x in ID_map[container].partitions:                
                        max_list.append(P[x])
                    
            #print(max_list)    
            weighted_error_values[container] = value * max(max_list)
                    
            # weighted_error_values[container] = value * max(
            #                                                 [
            #                                                 P[x] if ID_map[container].belongs == 1 
            #                                                 else default_weighted_error_parameter
            #                                                 for x in ID_map[container].partitions
            #                                                 ]
            #                                             )
    print("weighted error done")

    return weighted_error_values

def adjust_quota():
    weighted_error_value = weighted_error_values()
    if weighted_error_value:
        for cname,c_obj in ID_map.items():
            temp = c_obj.cpu_quota
            print(("quota", temp))
            if error_threshold > weighted_error_value[cname]:
                print(utilization_change_threshold, c_obj.utilization(), c_obj.cpu_quota, quota_lower_limit)
                if (utilization_change_threshold > c_obj.utilization()) and (c_obj.cpu_quota > quota_lower_limit):
                    print(c_obj.cpu_quota)
                    c_obj.cpu_quota -= quota_step*c_obj.cpu_quota
                    print(c_obj.cpu_quota)
            else:
                if c_obj.cpu_quota + quota_step*c_obj.cpu_quota < quota_upper_limit:
                    c_obj.cpu_quota += quota_step*c_obj.cpu_quota
            
            c_obj.cpu_quota = math.floor(c_obj.cpu_quota)
            # if there is a change in cpu quota
            if temp != c_obj.cpu_quota:
                print("change") 
                os.system(f"docker update --cpu-quota={c_obj.cpu_quota} {cname}")

def exec():
    flag = True
    while True:
        adjust_quota()
        print("adjusted")

exec()
