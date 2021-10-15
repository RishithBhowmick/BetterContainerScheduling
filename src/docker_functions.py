

def cpu_utilisation(container):
    container_stats = container.stats(stream=False)
    if 'system_cpu_usage' in  container_stats['precpu_stats'].keys():
        UsageDelta = container_stats['cpu_stats']['cpu_usage']['total_usage'] - container_stats['precpu_stats']['cpu_usage']['total_usage']
        #     # from informations : UsageDelta = 25382985593 - 25382168431

        SystemDelta = container_stats['cpu_stats']['system_cpu_usage'] - container_stats['precpu_stats']['system_cpu_usage']
    #     # from informations : SystemDelta = 75406420000000 - 75400410000000

        len_cpu = len(container_stats['cpu_stats']['cpu_usage']['percpu_usage'])
    #     # from my informations : len_cpu = 2


        percentage = (UsageDelta / SystemDelta) * len_cpu * 100
    #     # this is a little big because the result is : 0.02719341098169717

        percent = round(percentage, 2)
        if percent < 1:
            return 1
        else:
            return percent
    else:
         return None