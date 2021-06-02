#!/usr/bin/env bash
now=$(date +'%m-%d-%Y_%T')
sudo docker kill $(sudo docker ps -q) || true
sudo docker rm $(sudo docker ps -q -a) || true
sudo docker-compose -f SchedVizTest/HeavyContainer/docker-compose.yml down || true

# pin containers to core 1
sudo docker run -d --rm --cpuset-cpus="2,8" --network=my_server --name ipc_server_dns_name server
sudo docker run -d --rm --cpuset-cpus="2,8" --network=my_server client
sudo docker-compose -f SchedVizTest/HeavyContainer/docker-compose.yml up -d --scale heavycontainer=1
# sudo docker run -d --rm --cpuset-cpus="2,8" heavy

# containers can run using any core
# sudo docker run -d --rm --network=my_server --name ipc_server_dns_name server
# sudo docker run -d --rm --network=my_server client

sleep 5

containers=$(sudo docker ps -q)

echo "Enter detailed description of the purpose of this recording: "
read description

echo "description: " $description >> SchedVizTest/TraceRecordings/PID/$now.txt
echo "\n\n----------------------" $(date) "----------------------" >> SchedVizTest/TraceRecordings/PID/$now.txt
echo -e "\ndocker ps:" >> SchedVizTest/TraceRecordings/PID/$now.txt
echo -e $(sudo docker ps)'\n\n' >> SchedVizTest/TraceRecordings/PID/$now.txt
echo -e "docker top:\n" >> SchedVizTest/TraceRecordings/PID/$now.txt

for i in $containers; do
     sudo docker top $i >> SchedVizTest/TraceRecordings/PID/$now.txt
done

sleep 7

sudo SchedVizTest/schedviz/util/trace.sh -out "SchedVizTest/TraceRecordings/$now" -capture_seconds 15 -copy_timeout 10

sudo docker kill $(sudo docker ps -a -q)
sudo docker rm $(sudo docker ps -a -q)
sudo docker-compose -f SchedVizTest/HeavyContainer/docker-compose.yml down