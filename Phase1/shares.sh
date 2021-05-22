cd HeavyContainer
sudo docker-compose down
sleep 10
sudo docker-compose up -d --scale load=8
cd ..
cd Server
sudo docker run --rm --network=my_server --privileged --cap-add=ALL -v /dev:/dev -v /lib/modules:/lib/modules -v /proc/uptime:/proc/uptime --name ipc_server_dns_name server