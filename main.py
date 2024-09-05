import threading
from batch import json_batch, log_batch

trace_ids_dict = {}

# 각 batch를 실행할 스레드를 생성
thread1 = threading.Thread(target=log_batch.run_batch1)
thread2 = threading.Thread(target=json_batch.run_batch2)

# 스레드를 시작 (동시에 실행)
thread1.start()
thread2.start()