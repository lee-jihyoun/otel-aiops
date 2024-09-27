import threading
from batch import parser_batch, api_batch, complete_data_batch
import logging, time
from util.logging_config import setup_logging

setup_logging()
logging.info("**************** main.py start ****************")


thread1 = threading.Thread(target=parser_batch.filtered_log_parsing.redis_insert)  # 각 batch를 실행할 스레드를 생성
thread2 = threading.Thread(target=parser_batch.original_log_parsing.redis_insert)  # 각 batch를 실행할 스레드를 생성
thread3 = threading.Thread(target=parser_batch.filtered_trace_parsing.redis_insert)  # 각 batch를 실행할 스레드를 생성
thread4 = threading.Thread(target=parser_batch.original_trace_parsing.redis_insert)  # 각 batch를 실행할 스레드를 생성

# thread1 = threading.Thread(target=parser_batch.filtered_log_parsing.logparser)  # 각 batch를 실행할 스레드를 생성
# thread2 = threading.Thread(target=api_batch.main)
# thread3 = threading.Thread(target=complete_data_batch.main)

thread1.start()
thread2.start()
thread3.start()
thread4.start()

thread1.join() # 스레드가 종료될 때까지 대기
thread2.join()
thread3.join()
thread4.join()
