import docker
import pprint
import time
import json
import requests
from docker_functions import *
from datetime import datetime


queue = list()

def get_utilisation(container_name,container_list):
  req_container = [i for i in container_list if i.name==container_name]
  utilisation = get_utilisation(req_container[0])
  return utilisation



def findpartitions(partitions, nginx_index, parent_child, visited,graph,vertices):
  # curr_index = nginx_index
  queue.append([nginx_index, 0])
  partitions = [[vertices[nginx_index]]]

  while queue:
    # print(queue)
    curr_index, part_level = queue.pop(0)
    #print("Printing",parent_child[vertices[curr_index]])

    for i in range(len(vertices)):
      if graph[curr_index][i] == 1 and visited[i] != 1:        
          if parent_child[vertices[i]][1] <= parent_child[vertices[i]][0]:
            partitions[part_level].append(vertices[i])
            queue.append([i, part_level])

          else:
            temp = [vertices[i]]
            partitions.append(temp)
            queue.append([i, len(partitions)-1])
          visited[i] = 1
  # print(graph)
  return partitions
      
client = docker.from_env()
containers = client.containers.list()
vertices = [container.name for container in containers if container.name not in ["jaeger","prometheus","grafana"]]
# print(vertices)
vertices_no = len(vertices)
graph = [[0 for _ in range(len(vertices))] for _ in range(len(vertices))]

r = requests.get("http://34.83.243.141:16686/api/dependencies")


for item in r.json()["data"]:
  # sanitised_parent = item["parent"].split("-")
  # sanitised_parent = "-".join(sanitised_parent[:-1])
  # # print(sanitised_parent)
  # sanitised_child = item["child"].split("-")
  # sanitised_child = "-".join(sanitised_parent[:-1])
  # print(sanitised_parent)
  if item["parent"] == "nginx-web-server":
    item["parent"] = "nginx-thrift"
  if item["child"] == "nginx-web-server":
    item["child"] = "nginx-thrift"

  parent_service = [i for i in range(len(vertices)) if item["parent"] in vertices[i]]
  #print(parent_service)
  child_service = [i for i in range(len(vertices)) if item["child"] in vertices[i]]
  # print(child_service)
  # i1 = vertices.index(parent_service[0])
  # i2 = vertices.index(child_service[0])
  graph[parent_service[0]][child_service[0]] = 1  
  
parent_child = dict()
nginx_index = -1
for i in range(vertices_no):
  if "nginx" in vertices[i]:
    nginx_index = i
  for j in range(vertices_no):
    if graph[i][j] == 1:
      if vertices[i] not in parent_child:
        parent_child[vertices[i]] = [0, 1]
      else:
        parent_child[vertices[i]][1] += 1
      if vertices[j] not in parent_child:
        parent_child[vertices[j]] = [1, 0]
      else:
        parent_child[vertices[j]][0] += 1

partitions = []
visited=[0 for i in range(len(vertices))]
partitions = findpartitions(partitions, nginx_index,parent_child, visited,graph,vertices)

print(partitions)
utilisation_partitions = [[get_utilisation(container) for container in partition] for partition in partitions]
print(utilisation_partitions)




