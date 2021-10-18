import json
from numpy import mean
with open("all_workloads.json","r") as f:
    trace_data = json.loads(f.read())

# print(len(trace_data['data'][0]))
i=0
# all_spans = trace_data["data"][0]["spans"]
all_times = []
all_start_times = []
for trace in trace_data["data"]:
    # print(type(data))
    # print(data.keys())
    # print(data['spanID'],len(data['spans']),len(data['processes']))
    # if all_spans[i]["spanID"] == all_spans[i]["references"]["spanID"]:
    #     print("true")
    operation_times_2d = []
    start_time = []
    for span in trace["spans"]:
        if span["operationName"] == "/wrk2-api/post/compose" and span['duration']:
            operation_times_2d.append([span['duration'],span['startTime']])

        # if span["operationName"] == "/wrk2-api/post/compose" and span['startTime']:
            # start_time.append(span['startTime'])    
    try:
        print(trace["traceID"],max(operation_times_2d,key = lambda x:x[0]))
        all_times.append(max(operation_times_2d,key = lambda x:x[0]))
    except Exception:
        pass

    # try:
    #     print(trace["traceID"],min(start_time))
    #     all_start_times.append(min(start_time))
    # except Exception:
    #     pass
    i+=1

print("Mean: ",mean([i[0] for i in all_times]),"Length all times",len(all_times))

# data[0][spans][0][operationName]== "/wrk2-api/post-compose"