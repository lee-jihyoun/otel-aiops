import json, os
import time

import json_parser.log_parser as log_parser
from util.file_util import check_file_modified

import traceID.trace_id as trace_id
trace_id.trace_id_dict["log_batch"] = ""

def run_batch1():

    # 경로 설정
    input_path = '../data/testfolder/'
    output_path = '../data/testfolder/output/'
    file_name = 'test_logs.json'

    idx = 0

    log_parsing = log_parser.LogParsing(input_path=input_path,
                                        output_path=output_path,
                                        file_name=file_name,
                                        idx=idx)

    last_modified_time = os.path.getmtime(input_path + file_name)
    print(last_modified_time)

    while True:
        # file_name 파일 변경 여부 확인
        is_modified, last_modified_time = check_file_modified(input_path + file_name, last_modified_time)

        if is_modified:
            print("modified_print: ", trace_id.trace_id_dict)
            l = log_parsing.logparser()
            print(l[0]) # idx
            print(l[1]) # trace_ids
            print(l[2]) # filtered_log[]
            print("\n")

        time.sleep(1)