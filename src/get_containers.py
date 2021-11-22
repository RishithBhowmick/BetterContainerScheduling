import json
client = docker.from_env()
all_containers = client.containers.list()
from itertools import chain
with open("all_new_partitions.json","r") as f:
    all_partitions = json.loads(f.read())
#print(all_partitions)
all_partitions_with_ids = dict()
def get_containers_in_service(service_name,container_list):    
    #print(container_list)
    containers = list()
    for i in container_list:
      print(i.name)
    #   if service_name in i.name:
    #      containers.append(i.id)
    return containers
for key in all_partitions.keys():
    all_containers = [get_containers_in_service(container_name,all_containers) for container_name in all_partitions[key]]
    all_partitions_with_ids[key] = chain.from_iterable(all_containers)
#print(all_partitions_with_ids)
with open("all_new_partition_ids.json","w") as f:
    f.write(json.dumps(all_partitions_with_ids))
