import threading
from batch import parser_batch, api_batch
import psycopg2  # pip install psycopg2-binary
import re
import requests
import json
import variables.trace_id as trace_id

print("==============")
# trace_id_dict 테스트용
# trace_id.main_dict["main"] = ""
# print("main: ", trace_id.main_dict)

# thread1 = threading.Thread(target=parser_batch.run_batch1)  # 각 batch를 실행할 스레드를 생성
# thread1.start()  # 스레드를 시작 (동시에 실행)
# thread1.join()  # 스레드가 종료될 때까지 대기

thread2 = threading.Thread(target=api_batch.main)
thread2.start()  # 스레드를 시작 (동시에 실행)
thread2.join()  # 스레드가 종료될 때까지 대기