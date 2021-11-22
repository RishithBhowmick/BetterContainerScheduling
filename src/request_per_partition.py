import requests
call_count = requests.get("http://localhost:16686/api/dependencies").json()
partition_request = dict()
for item in call_count["data"]:
    if item["parent"] == "nginx-web-server":
        partition_request[item["child"]] = item["callCount"]
print(partition_request)