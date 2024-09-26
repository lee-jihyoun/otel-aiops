import threading
from batch import parser_batch, api_batch, complete_data_batch
import logging
from util.logging_config import setup_logging

setup_logging()
logging.info("**************** main.py start ****************")

# thread1 = threading.Thread(target=parser_batch.filtered_log_parsing.logparser)  # 각 batch를 실행할 스레드를 생성
# thread1 = threading.Thread(target=parser_batch.filtered_log_parsing.logparser)  # 각 batch를 실행할 스레드를 생성
# thread2 = threading.Thread(target=parser_batch.original_log_parsing.logparser)  # 각 batch를 실행할 스레드를 생성
thread2 = threading.Thread(target=api_batch.main)

# thread1.start()  # 스레드를 시작 (동시에 실행)
# thread1.start()  # 스레드를 시작 (동시에 실행)
thread2.start()  # 스레드를 시작 (동시에 실행)

# thread1.join()  # 스레드가 종료될 때까지 대기
# thread1.join()  # 스레드가 종료될 때까지 대기
thread2.join()  # 스레드가 종료될 때까지 대기


# while True:
#     parser_batch.filtered_log_parsing.logparser()
#     parser_batch.original_log_parsing.logparser()
#     parser_batch.filtered_trace_parsing.traceparser()
#     parser_batch.original_trace_parsing.traceparser()
#
#     time.sleep(1)

# while True:
#     complete_data_batch.process_complete_hash()
#     time.sleep(180) # 3분