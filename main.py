import threading
import batch1
import batch2

trace_id_dict = {}

# 각 batch를 실행할 스레드를 생성
thread1 = threading.Thread(target=batch1.run_batch1)
thread2 = threading.Thread(target=batch2.run_batch2)

# 스레드를 시작 (동시에 실행)
thread1.start()
thread2.start()