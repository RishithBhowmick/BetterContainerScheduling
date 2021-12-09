import requests
import json
from itertools import chain
import docker
client = docker.from_env()
all_containers = client.containers.list()

user_timeline_traces = requests.get("http://localhost:16686/api/traces?service=user-timeline-service").json()
compose_post_traces = requests.get("http://localhost:16686/api/traces?service=compose-post-service").json()
home_timeline_traces = requests.get("http://localhost:16686/api/traces?service=home-timeline-service").json()


user_timeline_trace = user_timeline_traces["data"][0]
home_timeline_trace = home_timeline_traces["data"][0]
compose_post_trace = compose_post_traces["data"][0]
# print(compose_post_traces)

dependencies = dict()
dependencies["user-timeline-service"] = [i['serviceName'] for i in user_timeline_trace["processes"].values()]
dependencies["home-timeline-service"] = [i['serviceName'] for i in home_timeline_trace["processes"].values()]
dependencies["compose-post-service"] = [i['serviceName'] for i in compose_post_trace["processes"].values()]

def get_container_from_name(container_name,container_list):    
  req_container = [i for i in container_list if i.name==container_name]  
  return req_container[0]


with open("all_new_partitions.json","w") as f:
    f.write(json.dumps(dependencies))

all_partitions_with_ids = dict()
def get_containers_in_service(service_name,container_list):        
   containers = [i.id for i in container_list if service_name in i.name]
   print(containers)
   return containers

for key in dependencies.keys():
    containers_for_service = [get_containers_in_service(container_name,all_containers) for container_name in dependencies[key]]
    all_partitions_with_ids[key] = list(chain.from_iterable(containers_for_service))    


print(all_partitions_with_ids)

with open("partition_with_ids.json","w") as f:
    f.write(json.dumps(all_partitions_with_ids))

# # first approach but data can exceed limit
# print(len(user_timeline_traces['data']))
# print(len(home_timeline_traces['data']))
# print(len(compose_post_traces['data']))

# 2nd approach 
# call_count = requests.get("http://34.127.122.253:16686/api/dependencies").json()
# for item in call_count["data"]:
#     if item["parent"] == "nginx-web-server":
#         print(item["child"],item["callCount"])
        