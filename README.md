# BetterContainerScheduling

* Build kernel module by running `make` in the "Server" directory. `init_module()` runs when module is inserted, and `cleanup_module()` is run when module is removed.
* Build server container with `sudo docker build -t server .`
* Run server with `sudo docker run --rm --network=my_server --privileged --cap-add=ALL -v /dev:/dev -v /lib/modules:/lib/modules -v /proc/uptime:/proc/uptime --name ipc_server_dns_name server`
* Build client with `sudo docker build -t client .`
* Run client with `sudo docker run --rm --network=my_server client`