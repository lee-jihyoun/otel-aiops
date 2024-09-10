import time
import traceID.trace_id as trace_id
trace_id_dict = trace_id.trace_id_dict

def run_batch2():
    while True:
        # for i in range(10000):
        #     trace_id_dict[i] = ""

        print("Hello World2")
        time.sleep(1)  # 1초 대기
