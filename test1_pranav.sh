#!/bin/bash
now=$(date +'%m-%d-%Y_%T')
sudo docker kill $(sudo docker ps -q) || true

# pin containers to core 1
sudo docker run -d --rm --cpuset-cpus="2,8" --network=my_server --name ipc_server_dns_name server
sudo docker run -d --rm --cpuset-cpus="2,8" --network=my_server client

# containers can run using any core
# sudo docker run -d --rm --network=my_server --name ipc_server_dns_name server
# sudo docker run -d --rm --network=my_server client

sleep 2

containers=$(sudo docker ps -q)

echo "----------------------" $(date) "----------------------" >>/home/pranav/Desktop/College/BetterContainerScheduling/SchedVizTest/TraceRecordings/PID/$now.txt
echo -e "\ndocker ps:" >>/home/pranav/Desktop/College/BetterContainerScheduling/SchedVizTest/TraceRecordings/PID/$now.txt
echo -e $(sudo docker ps)'\n\n' >>/home/pranav/Desktop/College/BetterContainerScheduling/SchedVizTest/TraceRecordings/PID/$now.txt
echo -e "docker top:\n" >>/home/pranav/Desktop/College/BetterContainerScheduling/SchedVizTest/TraceRecordings/PID/$now.txt

for i in $containers; do
    sudo docker top $i >>/home/pranav/Desktop/College/BetterContainerScheduling/SchedVizTest/TraceRecordings/PID/$now.txt
done

sleep 7

sudo sh /home/pranav/Desktop/College/BetterContainerScheduling/SchedVizTest/schedviz/util/trace.sh -out "/home/pranav/Desktop/College/BetterContainerScheduling/SchedVizTest/TraceRecordings/$now" -capture_seconds 15

sudo docker kill $(sudo docker ps -a -q)
sudo docker rm $(sudo docker ps -a -q)