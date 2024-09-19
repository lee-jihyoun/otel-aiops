import time, datetime
import json_parser.log_parser as log_parser
import json_parser.trace_parser as trace_parser
import variables.trace_id as trace_id
import variables.file_idx as file_idx

# # main_dict 테스트용
# trace_id.main_dict["total_batch"] = ""

def run_batch1():
    while True:
        # 경로 설정
        input_path = '../data/testfolder/'
        output_path = '../data/testfolder/output/'

        print("**************** 로그 파싱 시작 ****************")
        filtered_log = 'filtered_logs.json'
        original_log = 'original_logs.json'

        filtered_log_idx = file_idx.idx.get('filtered_logs')
        original_log_idx = file_idx.idx.get('original_logs')
        print("filtered_log_idx, original_log_idx: ", filtered_log_idx, original_log_idx)

        log_parsing = log_parser.LogParsing(input_path=input_path,
                                            output_path=output_path,
                                            filtered_file_name=filtered_log,
                                            original_file_name=original_log,
                                            filtered_idx=filtered_log_idx,
                                            original_idx=original_log_idx)

        log_parsing.filtered_logparser()
        print("**************** 로그 파싱 end :", datetime.datetime.now(), "****************")

        print("**************** 트레이스 파싱 시작 ****************")
        filtered_span = 'filtered_span.json'
        original_span = 'original_span.json'

        filtered_span_idx = file_idx.idx.get('filtered_span')
        original_span_idx = file_idx.idx.get('original_span')
        print("filtered_span_idx, original_span_idx: ", filtered_span_idx, original_span_idx)

        trace_parsing = trace_parser.TraceParsing(input_path=input_path,
                                                  output_path=output_path,
                                                  filtered_file_name=filtered_span,
                                                  original_file_name=original_span,
                                                  filtered_idx=filtered_span_idx,
                                                  original_idx=original_span_idx)

        trace_parsing.filtered_trace_parser()
        print("**************** 트레이스 파싱 end :", datetime.datetime.now(), "****************")

        time.sleep(0.5)