import threading
from batch import parser_batch, api_batch, complete_data_batch
import logging

logging.info("**************** main.py start ****************")

# 데이터 파싱
thread1 = threading.Thread(target=parser_batch.filtered_log_parsing.redis_insert)  # 각 batch를 실행할 스레드를 생성
thread2 = threading.Thread(target=parser_batch.original_log_parsing.redis_insert)  # 각 batch를 실행할 스레드를 생성
thread3 = threading.Thread(target=parser_batch.filtered_trace_parsing.redis_insert)  # 각 batch를 실행할 스레드를 생성
thread4 = threading.Thread(target=parser_batch.original_trace_parsing.redis_insert)  # 각 batch를 실행할 스레드를 생성
# complete_hash에 insert
thread5 = threading.Thread(target=complete_data_batch.main)
# mail 발송
thread6 = threading.Thread(target=api_batch.main)


# 데이터 파싱
thread1.start()
thread2.start()
thread3.start()
thread4.start()
# complete_hash에 insert
thread5.start()
# mail 발송
thread6.start()


# 데이터 파싱
thread1.join() # 스레드가 종료될 때까지 대기
thread2.join()
thread3.join()
thread4.join()
# complete_hash에 insert
thread5.join()
# mail 발송
thread6.join()
