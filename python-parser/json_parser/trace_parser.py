import configparser
import itertools
import json
import logging
import redis
from util.datetime_util import change_timenano_format

filter_last_position = 0
original_last_position = 0


class TraceParsing:

    def __init__(self, input_path, file_name):
        self.input_path = input_path
        self.file_name = file_name

    def get_redis_db_connection(self):
        config = configparser.ConfigParser()
        config.read('./config/db_config.ini')
        host = config['redis-DB']['DB_HOST']
        port = config['redis-DB']['DB_PORT']
        pwd = config['redis-DB']['DB_PWD']
        db_num = config['redis-DB']['DB']
        conn = redis.Redis(host=host, port=port, decode_responses=True, db=db_num, password=pwd)
        return conn

    def traceparser(self):
        input_path = self.input_path
        file_name = self.file_name

        global filter_last_position, original_last_position
        parsing_trace_data_list = [] # "a111", "b111"

        with open(input_path + file_name, "r") as log_file:
            # # logging.info("filter_last_position")
            # # logging.info(filter_last_position)

            if file_name == "filtered_span.json":
                idx = filter_last_position
            else:
                idx = original_last_position

            for current_index, line in enumerate(itertools.islice(log_file, idx, None), start=idx):

                # # logging.info("===========================")
                # # logging.info(line)

                if not line:  # 더 이상 읽을 데이터가 없으면
                    # # logging.info("데이터가 없습니다")
                    break  # 루프를 종료

                else:
                    # # logging.info(f"================ filtered_span 파싱 start: {datetime.datetime.now()} ================")

                    try:
                        span_data = json.loads(line.strip())
                        change_timenano_format(span_data)

                        for resource in span_data.get('resourceSpans', []):
                            service_name = None
                            service_code = None
                            os_type = None

                            # if "resource" in resource and "attributes" in resource["resource"]:
                            if "resource" in resource and "attributes" in resource["resource"]:
                                for attribute in resource["resource"]["attributes"]:
                                    if attribute["key"] == "service.name":
                                        service_name = attribute["value"]["stringValue"].replace('"', '')
                                    if attribute["key"] == "service.code":
                                        service_code = attribute["value"]["stringValue"].replace('"', '')
                                    if attribute["key"] == "os.type":
                                        os_type = attribute["value"]["stringValue"].replace('"', '')
                            # trace_parser에서 for scope_span in resource.get("scopeSpans", []):
                            for scopeSpan in resource.get("scopeSpans", []):
                                for span in scopeSpan.get("spans", []):
                                    # trace에서는 scopespan 안에 attribute가 따로 있음
                                    for attribute in span.get("attributes", []):
                                        parsed_info = {
                                            "service.name": service_name,
                                            "service.code": service_code,
                                            "os.type": os_type,
                                            "traceId": span.get("traceId"),
                                            "spanId": span.get("spanId"),
                                            "name": span.get("name"),
                                            "http.status_code": None,
                                            "rpc.grpc.status_code": None,
                                            "trace.exception.message": None,
                                            "trace.exception.stacktrace": None,
                                            "trace.exception.stacktrace.short": None,
                                            "trace.exception.type": None,
                                            "http.url": None,
                                            "rpc.method": None,
                                            "startTimeUnixNano": span.get("startTimeUnixNano"),
                                            "endTimeUnixNano": span.get("endTimeUnixNano")
                                        }

                                        try:
                                            if attribute["key"] == "http.status_code" and "intValue" in attribute["value"]:
                                                parsed_info["http.status_code"] = attribute["value"]["intValue"]
                                            if attribute["key"] == "rpc.grpc.status_code":
                                                parsed_info["rpc.grpc.status_code"] = attribute["value"]["intValue"]
                                            if attribute["key"] == "http.url":
                                                parsed_info["http.url"] = attribute["value"]["stringValue"].replace('"', '')
                                            if attribute["key"] == "rpc.method":
                                                parsed_info["rpc.method"] = attribute["value"]["stringValue"].replace('"', '')
                                        except KeyError as e:
                                            logging.ERROR(f"Key is not found: {e}")
                                            continue
                                    # event 발생 시 event key 내에 exception.message와 exception.stacktrace가 따로 있음
                                    for event in span.get("events", []):
                                        for attribute in event.get("attributes", []):
                                            if attribute["key"] == "exception.message":
                                                parsed_info["trace.exception.message"] = attribute["value"]["stringValue"].replace('"', '')
                                            if attribute["key"] == "exception.stacktrace":
                                                parsed_info["trace.exception.stacktrace"] = attribute["value"]["stringValue"].replace('"', '')
                                                # 두 번째 \n 전까지만 가져오기, 중간에 \n 존재 시 삭제
                                                parsed_info["trace.exception.stacktrace.short"] = ' '.join(line.strip() for line in attribute["value"]["stringValue"].split('\n')[:2]).replace('"', '')
                                            if attribute["key"] == "exception.type":
                                                parsed_info["trace.exception.type"] = attribute["value"]["stringValue"].replace('"', '')

                                    # span이 여러개인 경우 list에 파싱 결과를 append하여 전달
                                    parsing_trace_data_list.append(parsed_info)

                    except json.JSONDecodeError as e:
                        logging.ERROR(f"Error parsing line: {e}")

                    # # logging.info("parsing_trace_data_list\n")
                    # # logging.info(parsing_trace_data_list)
                    # # logging.info(len(parsing_trace_data_list))

                    # 마지막으로 읽은 위치를 업데이트
                    if file_name == "filtered_span.json":
                        # 파일 포인터를 마지막 읽은 위치로 이동
                        filter_last_position = current_index + 1

                    else:
                        original_last_position = current_index + 1

                    # # logging.info("============ trace 파싱 end ===========\n")
                    logging.info(parsing_trace_data_list)

                return parsing_trace_data_list

    def redis_insert(self):
        # Redis 클라이언트 설정
        r = self.get_redis_db_connection()

        while True:

            file_name = self.file_name
            parsing_trace_data_list = self.traceparser()

            # # logging.info("**************************")
            # # logging.info("parsing_trace_data_list\n")
            # # logging.info(parsing_trace_data_list)
            # # logging.info("**************************")

            if parsing_trace_data_list != None:
                # # logging.info("============ db 삽입 start===========\n")

                # # list 형태로 저장
                for trace in parsing_trace_data_list:

                    trace_id = trace['traceId']
                    retry_count_store = "retry_count_store:" + trace_id

                    if file_name == "filtered_span.json":
                        # 전체 키는 traceId로 설정
                        key_list = f"filtered_trace_list:{trace_id}"

                    else:
                        # 전체 키는 traceId로 설정
                        key_list = f"original_trace_list:{trace_id}"
                        retry_count_store = "retry_count_store:" + trace_id

                    trace = str(trace)

                    r.rpush(key_list, trace)
                    r.expire(key_list, 60 * 15)  # 60s * 15 = 15m

                    # logging.info(f"* full_key: {key_list}")
                    # logging.info(f"* trace: {trace}")

                    r.sadd("key_store",trace_id)
                    # r.rpush("key_store", trace_id)
                    r.expire("key_store", 60 * 15)  # 60s * 15 = 15m

                    # logging.info(f"* key_store: {trace_id}")
                    #
                    # r.hset(retry_count_store, "retry", "0")
                    # r.expire(retry_count_store, 60*15)
                    #
                    # # logging.info(f"* retry_count_store: {retry_count_store}")