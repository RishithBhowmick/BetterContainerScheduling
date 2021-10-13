import docker
import pprint
import time
client = docker.from_env()
all_containers = client.containers.list()
while True:
    for container in all_containers:    
        # pprint.pprint(container.attrs['HostConfig']['CpuShares'])
        # container.update(cpu_shares=2)
        # client.refresh()
        # pprint.pprint(container.attrs['HostConfig']['CpuShares'])
        # container_stats = container.stats(stream=False)
        # pprint.pprint(container_stats)
        # print("&&&&&&&&&&")
        # container_stats = container.stats(decode=True,stream=False)
        container_stats = container.stats(stream=False)
        # print(container.name)
        # pprint.pprint(container_stats['cpu_stats'])
        # for i in container_stats:
        #     pprint.pprint(i['cpu_stats'])
        #     pprint.pprint(i['precpu_stats'])

        if 'system_cpu_usage' in  container_stats['precpu_stats'].keys():
            # print(i.keys())
            UsageDelta = container_stats['cpu_stats']['cpu_usage']['total_usage'] - container_stats['precpu_stats']['cpu_usage']['total_usage']
        #     # from informations : UsageDelta = 25382985593 - 25382168431

            SystemDelta = container_stats['cpu_stats']['system_cpu_usage'] - container_stats['precpu_stats']['system_cpu_usage']
        #     # from informations : SystemDelta = 75406420000000 - 75400410000000

            len_cpu = len(container_stats['cpu_stats']['cpu_usage']['percpu_usage'])
        #     # from my informations : len_cpu = 2


            percentage = (UsageDelta / SystemDelta) * len_cpu * 100
        #     # this is a little big because the result is : 0.02719341098169717

            percent = round(percentage, 2)
            print(container.name,percent)            
        else:            
            pass
        #     time.sleep(3)
            #     # now The output is 0.02 and thats the answer.
    time.sleep(3)