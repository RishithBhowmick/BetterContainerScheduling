#!/usr/bin/env bash
now=$(date +'%m-%d-%Y_%T')
sudo docker kill $(sudo docker ps -q) || true
sudo docker-compose down || true

# pin containers to core 1
sudo docker run -d --rm --cpuset-cpus="2,6" --network=my_server --name ipc_server_dns_name server
sudo docker run -d --rm --cpuset-cpus="2,6" --network=my_server client
cd /home/ishi/Capstone/BetterContainerScheduling/SchedVizTest/HeavyContainer
sudo docker-compose up -d --scale heavycontainer=1
# containers can run using any core
# sudo docker run -d --rm --network=my_server --name ipc_server_dns_name server
# sudo docker run -d --rm --network=my_server client

sleep 5

containers=$(sudo docker ps -q)

echo "Enter detailed description of the purpose of this recording: "
read description

echo "description: " $description >> /home/ishi/Capstone/BetterContainerScheduling/SchedVizTest/TraceRecordings/PID/$now.txt
echo "\n\n----------------------" $(date) "----------------------" >> /home/ishi/Capstone/BetterContainerScheduling/SchedVizTest/TraceRecordings/PID/$now.txt
echo -e "\ndocker ps:" >> /home/ishi/Capstone/BetterContainerScheduling/SchedVizTest/TraceRecordings/PID/$now.txt
echo -e $(sudo docker ps)'\n\n' >> /home/ishi/Capstone/BetterContainerScheduling/SchedVizTest/TraceRecordings/PID/$now.txt
echo -e "docker top:\n" >> /home/ishi/Capstone/BetterContainerScheduling/SchedVizTest/TraceRecordings/PID/$now.txt

for i in $containers; do
     sudo docker top $i >> /home/ishi/Capstone/BetterContainerScheduling/SchedVizTest/TraceRecordings/PID/$now.txt
done

sleep 7

sudo /home/ishi/Capstone/schedviz/util/trace.sh -out "/home/ishi/Capstone/BetterContainerScheduling/SchedVizTest/TraceRecordings/$now" -capture_seconds 15 -copy_timeout 10

sudo docker kill $(sudo docker ps -a -q)
sudo docker rm $(sudo docker ps -a -q)
sudo docker-compose down
