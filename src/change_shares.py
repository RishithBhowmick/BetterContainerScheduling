import docker
import pprint
import time
from docker_functions import *


client = docker.from_env()
all_containers = client.containers.list()

while True:
    container_utilisation_dict = dict()
    for container in all_containers:    
        container_stats = container.stats(stream=False)
        if "jaeger" in container.name and "grafana" in container.name and "prometheus" in container.name:
            continue    

        if 'system_cpu_usage' in  container_stats['precpu_stats'].keys():
            percent = cpu_utilisation(container_stats)
            container_utilisation_dict[container] = percent             
        else:            
            pass
                
    try:    
                
        average_utilisation = sum(container_utilisation_dict.values())/len(container_utilisation_dict)         
        for container,utilisation in container_utilisation_dict.items():
            # pprint.pprint(container.attrs['HostConfig']['CpuShares'])
            new_shares = (1024/utilisation)*average_utilisation             
            print("Name: ",container.name,"Utilisation: ",utilisation,"shares ",new_shares)               
            container.update(cpu_shares = new_shares)
    # print(container_utilisation_dict)
    except Exception as e:
        print(str(e),e._traceback_.tb_lineno)
    time.sleep(5)