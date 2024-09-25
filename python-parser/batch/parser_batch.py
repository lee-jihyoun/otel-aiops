import datetime
import json_parser.log_parser as log_parser
import logging

# 경로 설정(local에서 테스트 시)
input_path = '../data/servertest/'

# 경로 설정(서버에서 테스트 시)
# input_path = '/opt/spring-otel-listener-run/'

logging.info("**************** 로그 파싱 시작 ****************")
filtered_log = 'filtered_logs.json'
original_log = 'original_logs.json'

# thread로 돌려야 함
filtered_log_parsing = log_parser.LogParsing(input_path=input_path,
                                             file_name=filtered_log)
# thread로 돌려야 함
original_log_parsing = log_parser.LogParsing(input_path=input_path,
                                             file_name=original_log)

logging.info(f"================ 로그 파싱 end: {datetime.datetime.now()} ================")

        #
        # logging.info("**************** 트레이스 파싱 시작 ****************")
        # filtered_span = 'filtered_span.json'
        # original_span = 'original_span.json'
        #
        # filtered_span_idx = file_idx.idx.get('filtered_span')
        # original_span_idx = file_idx.idx.get('original_span')
        # logging.info(f"* filtered_span_idx: {filtered_span_idx}")
        # logging.info(f"* original_span_idx: {original_span_idx}")
        #
        # trace_parsing = trace_parser.TraceParsing(input_path=input_path,
        #                                           filtered_file_name=filtered_span,
        #                                           original_file_name=original_span,
        #                                           filtered_idx=filtered_span_idx,
        #                                           original_idx=original_span_idx)
        #
        # trace_parsing.filtered_trace_parser()
        # logging.info(f"**************** 트레이스 파싱 end: {datetime.datetime.now()} ****************")