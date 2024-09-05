import json, os
import time

import json_parser.log_parser as log_parser
from util.file_util import check_file_modified

# 경로 설정
input_path = './data/testfolder/'
output_path = './data/testfolder/output/'
file_name = 'test_logs.json'


with open(input_path + "trace_id_dict.json", "r", encoding='utf-8') as json_file:
    trace_ids_dict = json.load(json_file)
# 읽어온 데이터를 출력해 보기
print(trace_ids_dict)

log_parsing = log_parser.LogParsing(input_path=input_path,
                                    output_path=output_path,
                                    file_name=file_name,
                                    trace_ids_dict=trace_ids_dict)

last_modified_time = os.path.getmtime(input_path + file_name)
print(last_modified_time)

while True:
    # file_name 파일 변경 여부 확인
    is_modified, last_modified_time = check_file_modified(input_path + file_name, last_modified_time)

    if is_modified:
        l = log_parsing.logparser()
        print(l[0])
        print(l[1])

    time.sleep(1)

# def run_batch1():
#     log_parser()
#     # while True:
#     #     print("Hello World1")
#     #     time.sleep(1)  # 1초 대기
#
# run_batch1()