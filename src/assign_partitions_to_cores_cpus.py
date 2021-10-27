import docker
import pprint
import time
from docker_functions import *
from  concurrent.futures import ThreadPoolExecutor,as_completed
from datetime import datetime
import json 
import os,math  
num_cores = os.cpu_count()

client = docker.from_env()
all_containers = client.containers.list()
num_containers = len(all_containers)
with open("partitions.json","r") as f:
    partitions = json.loads(f.read())

containers_in_partition = {partition:[get_container_from_name(container,all_containers) for container in partitions[partition]] for partition in partitions.keys()}

print(containers_in_partition)
while True:
    container_utilisation_dict = dict()           

    with ThreadPoolExecutor(max_workers=num_containers) as executor:
        future_to_utilisation = {executor.submit(cpu_utilisation,container):container for container in all_containers if ("jaeger" not in container.name and "grafana" not in container.name and "prometheus" not in container.name)}

    for future in as_completed(future_to_utilisation):
            container_utilisation_dict[future_to_utilisation[future]] = future.result()                

    try:    
                
        #average_utilisation = sum(container_utilisation_dict.values())/len(container_utilisation_dict) 
        
        

        partition_utilisation = {partition:sum([container_utilisation_dict[get_container_from_name(container,all_containers)] for container in partitions[partition]]) for partition in partitions.keys()}
        print(partition_utilisation)
        
        shares_per_partition = {partition:(partition_utilisation[partition]/sum(partition_utilisation.values()))*1024 for partition in partition_utilisation.keys()}
        print(shares_per_partition)
        
        core_no = 0
        for partition,containers in containers_in_partition.items():   
            required_cores = round((partition_utilisation[partition]/sum(partition_utilisation.values()))*num_cores)


            for container in containers:
                new_cpus = round((container_utilisation_dict[container]/partition_utilisation[partition])*required_cores)
                print(container,new_cpus)
                # container.update(cpuset_cpus = f"{core_no}-{core_no+required_cores-1}")
                os.system(f"docker update --cpus={new_cpus} --cpuset-cpus={core_no}-{core_no+required_cores-1} {container.id}")
            core_no+=required_cores

        # minimum_utilisation = container_utilisation_dict[min(container_utilisation_dict,key = container_utilisation_dict.get)]  
        # for container,utilisation in container_utilisation_dict.items():
        #     # pprint.pprint(container.attrs['HostConfig']['CpuShares'])
        #     new_shares = (utilisation/minimum_utilisation)*2             
        #     print("Name: ",container.name,"| Utilisation: ",utilisation,"| shares ",new_shares)               
        #     container.update(cpu_shares = int(new_shares))
    # print(container_utilisation_dict)
        print("*****")
    except Exception as e:
        print(str(e),e.__traceback__.tb_lineno)
        pass
    time.sleep(10)
