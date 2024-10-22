import datetime, logging
import json_parser.log_parser as log_parser
import json_parser.trace_parser as trace_parser



# 경로 설정(local에서 테스트 시)
input_path = '../data/20241022_success_case/'

# 경로 설정(서버에서 테스트 시)
# input_path = '/opt/spring-otel-listener-run/'

logging.info("**************** 로그 파싱 시작 ****************")
filtered_log = 'filtered_logs.json'
original_log = 'original_logs.json'

filtered_log_parsing = log_parser.LogParsing(input_path=input_path,
                                             file_name=filtered_log)
original_log_parsing = log_parser.LogParsing(input_path=input_path,
                                             file_name=original_log)

logging.info(f"================ 로그 파싱 end: {datetime.datetime.now()} ================")


logging.info("**************** 트레이스 파싱 시작 ****************")
filtered_span = 'filtered_span.json'
original_span = 'original_span.json'

filtered_trace_parsing = trace_parser.TraceParsing(input_path=input_path,
                                                   file_name=filtered_span)
original_trace_parsing = trace_parser.TraceParsing(input_path=input_path,
                                                   file_name=original_span)

logging.info(f"**************** 트레이스 파싱 end: {datetime.datetime.now()} ****************")