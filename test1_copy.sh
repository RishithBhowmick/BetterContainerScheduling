#!/usr/bin/env bash
now=$(date +'%m-%d-%Y_%T')
sudo docker kill $(sudo docker ps -q) || true

# pin containers to core 1
sudo docker run -d --rm --cpuset-cpus="1" --network=my_server --name ipc_server_dns_name server
sudo docker run -d --rm --cpuset-cpus="1" --network=my_server client

# containers can run using any core
# sudo docker run -d --rm --network=my_server --name ipc_server_dns_name server
# sudo docker run -d --rm --network=my_server client

sleep 2

containers=$(sudo docker ps -q)

echo "----------------------" $(date) "----------------------" >> /home/ishi/Capstone/BetterContainerScheduling/SchedVizTest/PID/docker_pid_$now.txt
echo -e "\ndocker ps:">> /home/ishi/Capstone/BetterContainerScheduling/SchedVizTest/PID/docker_pid_$now.txt
echo -e $(sudo docker ps)'\n\n' >> /home/ishi/Capstone/BetterContainerScheduling/SchedVizTest/PID/docker_pid_$now.txt
echo -e "docker top:\n">> /home/ishi/Capstone/BetterContainerScheduling/SchedVizTest/PID/docker_pid_$now.txt

for i in $containers
    do
        sudo docker top $i >> /home/ishi/Capstone/BetterContainerScheduling/SchedVizTest/PID/docker_pid_$now.txt
    done

sleep 7

sudo /home/ishi/Capstone/schedviz/util/trace.sh -out "/home/ishi/Capstone/BetterContainerScheduling/SchedVizTest/" -capture_seconds 15 

