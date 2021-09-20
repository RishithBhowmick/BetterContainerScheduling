# Copyright (c) Pixie Labs, Inc.
# Licensed under the Apache License, Version 2.0 (the "License")
import pxtrace
import px


program = """
#include <uapi/linux/ptrace.h>
#include <linux/sched.h>
#include <linux/nsproxy.h>
#include <linux/pid_namespace.h>



tracepoint:sched:sched_wakeup,
tracepoint:sched:sched_wakeup_new 
{
    @qtime[args->pid] = nsecs;
}

tracepoint:sched:sched_switch {
    
    if (args->prev_state == TASK_RUNNING) {
        if (args->prev_pid != 0) {
            @qtime[args->prev_pid] = nsecs;
        }
    }

    $ns = @qtime[args->next_pid];
    $latency = (nsecs - $ns)/1000;

    if($latency != 0 && args->next_pid != 0 && args->prev_pid != 0){
        printf(\"time_:%d oproc:%s opid:%d lat:%lld nproc:%s npid:%d\", nsecs, args->prev_comm, args->prev_pid, $latency, args->next_comm, args->next_pid);
    }

    delete(@qtime[args->next_pid]);    
}

"""

def demo_func():
    table_name = 'latencies_table'
    pxtrace.UpsertTracepoint('latencies_probe_2111',
                             table_name,
                             program,
                             pxtrace.kprobe(),
                             "10m")
    # Rename columns
    df = px.DataFrame(table=table_name)

    return df   

df = demo_func()

px.display(df)