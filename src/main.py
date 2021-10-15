import docker
import pprint
import time
from docker_functions import *
from datetime import date, datetime
from  concurrent.futures import ThreadPoolExecutor,as_completed
import os


client = docker.from_env()
all_containers = client.containers.list()
# print(all_containers)
# container_utilisation_dict = SortedDict()
num_containers = len(all_containers)
while True:
    container_utilisation_dict = dict()
    start_time = datetime.now()        
    with ThreadPoolExecutor(max_workers=num_containers) as executor:
        future_to_utilisation = {executor.submit(cpu_utilisation,container):container for container in all_containers}
        
        for future in as_completed(future_to_utilisation):
            container_utilisation_dict[future_to_utilisation[future]] = future.result()

    print(container_utilisation_dict)
    end_time = datetime.now()
    print(end_time-start_time)
    # for container in all_containers:    
        # pprint.pprint(container.attrs['HostConfig'])
        # container.update(cpu_shares=2)
        # client.refresh()
        # pprint.pprint(container.attrs['HostConfig']['CpuShares'])
        # container_stats = container.stats(stream=False)
        # pprint.pprint(container_stats)
        # print("&&&&&&&&&&")
        # container_stats = container.stats(decode=True,stream=False)
        # start_time = datetime.now()        
        # container_stats = container.stats(stream=False)
        # end_time = datetime.now()
        # print(container.name,end_time-start_time)
        # print(container.name)
        # pprint.pprint(container_stats['cpu_stats'])
        # for i in container_stats:
        #     pprint.pprint(i['cpu_stats'])
        #     pprint.pprint(i['precpu_stats'])
        # if "jaeger" in container.name and "grafana" in container.name and "prometheus" in container.name:
        #     continue    

        # if 'system_cpu_usage' in  container_stats['precpu_stats'].keys():
        #     # print(i.keys())
        #     percent = cpu_utilisation(container_stats)
        #     # print(container.name,percent)            
        #     if percent < 1:            
        #         container_utilisation_dict[container] = 1.0
        #     else:
        #         container_utilisation_dict[container] = percent
        #     # print(container.name)
        #     # pprint.pprint(container.attrs['HostConfig']['CpuShares'])
            
        # else:            
        #     pass
        #     time.sleep(3)
            #     # now The output is 0.02 and thats the answer.
    # number of cores
    # sum the utilisation of all containers
    # get the 'nano_cpus' value by (utilisation/sum)*num_cores
    # then assign
    
    try:
        # valid_containers = {key:value for key,value in container_utilisation_dict.items() if key != 0}     
        # minimum_utilisation = container_utilisation_dict[min(container_utilisation_dict,key = container_utilisation_dict.get)]
        total_utilisation = sum(container_utilisation_dict.values())
        num_cores = os.cpu_count()
        print(container_utilisation_dict)
        start_time = datetime.now()
        for container,utilisation in container_utilisation_dict.items():
            # pprint.pprint(container.attrs['HostConfig']['CpuShares'])            
            cpus = ((utilisation/total_utilisation)*num_cores)
            print(container.name,cpus)            
            # container.update(NanoCPUs = cpus)
            os.system(f"docker update --cpus={cpus} {container.id}")
        # print(container_utilisation_dict)
        end_time = datetime.now()
        print(end_time-start_time)
    except Exception as e:
        print("first iteration",str(e),e.__traceback__.tb_lineno)
    time.sleep(5)