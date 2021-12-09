import json
import docker
client = docker.from_env()
all_containers = client.containers.list()
all_containers
from itertools import chain
with open("all_new_partitions.json","r") as f:
    all_partitions = json.loads(f.read())
#print(all_partitions)


all_partitions_with_ids = dict()
def get_containers_in_service(service_name,container_list):        
   containers = [i.id for i in container_list if service_name in i.name]
   print(containers)
   return containers

for key in all_partitions.keys():
    containers_for_service = [get_containers_in_service(container_name,all_containers) for container_name in all_partitions[key]]
    all_partitions_with_ids[key] = list(chain.from_iterable(containers_for_service))    


print(all_partitions_with_ids)

with open("all_new_partition_ids.json","w") as f:
    f.write(json.dumps(all_partitions_with_ids))
