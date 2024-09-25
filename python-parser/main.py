import threading
from batch import parser_batch, api_batch, complete_data_batch
import psycopg2  # pip install psycopg2-binary
import re
import requests
import json
import logging
import time

# 로그 설정
'''
DEBUG: 프로그램 작동에 대한 상세한 정보를 나타내는 로그로 문제의 원인을 파악할 때 사용
INFO: 프로그램 작동이 예상대로 진행되고 있는지 파악하기 위해 사용
WARNING: 추후에 발생 가능한 문제를 나타내기 위해 사용
ERROR : 프로그램이 의도한 기능을 수행하지 못하고 있는 상황을 나타내기 위해 사용
CRITICAL : 프로그램 실행 자체가 중단될 수 있음을 나타내기 위해 사용
'''
logging.basicConfig(
    level=logging.INFO,
    format="[%(asctime)s | %(levelname)s] %(message)s",
    datefmt="%Y-%m-%d %H:%M:%S",
    handlers=[
        logging.FileHandler("python-parser.log"),
        logging.StreamHandler()  # 콘솔 출력용 핸들러
    ]
)

logging.info("**************** main.py start ****************")

while True:
    parser_batch.filtered_log_parsing.logparser()
    parser_batch.original_log_parsing.logparser()
    parser_batch.filtered_trace_parsing.traceparser()
    parser_batch.original_trace_parsing.traceparser()

    time.sleep(1)

# while True:
#     complete_data_batch.process_complete_hash()
#     time.sleep(180) # 3분