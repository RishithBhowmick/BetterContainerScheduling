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
if True:
    container_utilisation_dict = dict()
    start_time = datetime.now()        
    with ThreadPoolExecutor(max_workers=num_containers) as executor:
        future_to_utilisation = {executor.submit(cpu_utilisation,container):container for container in all_containers}
        
        for future in as_completed(future_to_utilisation):
            container_utilisation_dict[future_to_utilisation[future]] = future.result()

    print(container_utilisation_dict)
    end_time = datetime.now()
    print(end_time-start_time)
    
    try:
        total_utilisation = sum(container_utilisation_dict.values())
        num_cores = os.cpu_count()
        print(container_utilisation_dict)
        start_time = datetime.now()
        for container,utilisation in container_utilisation_dict.items():
            print("test",end=" ")
            pprint.pprint(container.attrs['HostConfig']['CpuPeriod'])
            #cpus = ((utilisation/total_utilisation)*num_cores)
            #cpus = round(cpus,2)       
            #print("Name: ",container.name,"Utilisation: ",utilisation,"New cpus: ",cpus)  
            #container.update(NanoCPUs = cpus)
            os.system(f"docker update --cpu-period=50000 {container.id}")
        # print(container_utilisation_dict)
        end_time = datetime.now()
        print(end_time-start_time)
    except Exception as e:
        print(str(e),e.__traceback__.tb_lineno)
