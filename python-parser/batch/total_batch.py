import time
import json_parser.log_parser as log_parser
import variables.trace_id as trace_id
import variables.file_idx as file_idx

# trace_id_dict 테스트용
trace_id.trace_id_dict["total_batch"] = ""

def run_batch1():

    # 경로 설정
    input_path = '../data/testfolder/'
    output_path = '../data/testfolder/output/'

    filtered_log = 'filtered_logs.json'
    original_log = 'original_logs.json'

    filtered_idx = file_idx.idx.get('filtered_logs')
    original_idx = file_idx.idx.get('original_logs')

    filtered_log_parsing = log_parser.LogParsing(input_path=input_path,
                                                output_path=output_path,
                                                file_name=filtered_log,
                                                idx=filtered_idx)

    parsed_filtered_log = filtered_log_parsing.logparser()

    # index 업데이트
    new_filtered_index = parsed_filtered_log[0]
    file_idx.idx[filtered_log[:-5]] = new_filtered_index

    if parsed_filtered_log[1] == []:
        original_log_parsing = log_parser.LogParsing(input_path=input_path,
                                                    output_path=output_path,
                                                    file_name=original_log,
                                                    idx=original_idx)

        parsed_original_log = original_log_parsing.logparser()

        new_original_index = parsed_original_log[0]
        file_idx.idx[filtered_log[:-5]] = new_original_index

        print(parsed_original_log[0])  # idx
        print(parsed_original_log[1])  # filtered_log[]



    time.sleep(10)