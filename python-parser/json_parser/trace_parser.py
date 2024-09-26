import json, itertools, datetime
from util.datetime_util import change_timenano_format
import logging, redis, time

filter_last_position = 0
original_last_position = 0

class TraceParsing:

    def __init__(self, input_path, file_name):
        self.input_path = input_path
        self.file_name = file_name

    def traceparser(self):
        input_path = self.input_path
        file_name = self.file_name

        global filter_last_position, original_last_position

        parsing_trace_data_list = [] # "a111", "b111"
        with open(input_path + file_name, "r") as log_file:
            # logging.info(last_position)
            if file_name == "filtered_logs.json":
                # 파일 포인터를 마지막 읽은 위치로 이동
                log_file.seek(filter_last_position)
            else:
                log_file.seek(original_last_position)

            while True:
                line = log_file.readline()  # 한 줄씩 읽기
                # logging.info("===========================")
                # logging.info(line)

                if not line:  # 더 이상 읽을 데이터가 없으면
                    logging.info("데이터가 없습니다")
                    break  # 루프를 종료

                # # 디버깅할 때 사용..
                # logging.info('* 아무 글자나 입력:')
                # input()
                else:
                    logging.info(f"================ filtered_span 파싱 start: {datetime.datetime.now()} ================")
                    # # 디버깅할 때 사용..
                    # logging.info('* 아무 글자나 입력:')
                    # input()

                    try:
                        span_data = json.loads(line.strip())
                        change_timenano_format(span_data)

                        for resource in span_data.get('resourceSpans', []):
                            service_name = None
                            service_code = None
                            os_type = None

                            # if "resource" in resource_log and "attributes" in resource_log["resource"]:
                            if "resource" in resource and "attributes" in resource["resource"]:
                                for attribute in resource["resource"]["attributes"]:
                                    if attribute["key"] == "service.name":
                                        service_name = attribute["value"]["stringValue"]
                                    if attribute["key"] == "service.code":
                                        service_code = attribute["value"]["stringValue"]
                                    if attribute["key"] == "os.type":
                                        os_type = attribute["value"]["stringValue"]
                            # log_parser에서 for scope_log in resource_log.get("scopeLogs", []):
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
                                            "exception.message": None,
                                            "exception.stacktrace": None,
                                            "exception.stacktrace.short": None,
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
                                                parsed_info["http.url"] = attribute["value"]["stringValue"]
                                            if attribute["key"] == "rpc.method":
                                                parsed_info["rpc.method"] = attribute["value"]["stringValue"]
                                        except KeyError as e:
                                            logging.ERROR(f"Key is not found: {e}")
                                            continue
                                    # event 발생 시 event key 내에 exception.message와 exception.stacktrace가 따로 있음
                                    for event in span.get("events", []):
                                        for attribute in event.get("attributes", []):
                                            if attribute["key"] == "exception.message":
                                                parsed_info["exception.message"] = attribute["value"]["stringValue"]
                                            if attribute["key"] == "exception.stacktrace":
                                                parsed_info["exception.stacktrace"] = attribute["value"]["stringValue"]
                                                # 두 번째 \n 전까지만 가져오기, 중간에 \n 존재 시 삭제
                                                parsed_info["exception.stacktrace.short"] = ' '.join(line.strip() for line in attribute["value"]["stringValue"].split('\n')[:2])

                                    # span이 여러개인 경우 list에 파싱 결과를 append하여 전달
                                    parsing_trace_data_list.append(parsed_info)

                    except json.JSONDecodeError as e:
                        logging.ERROR(f"Error parsing line: {e}")

                logging.info("parsing_trace_data_list\n")
                logging.info(parsing_trace_data_list)
                logging.info(len(parsing_trace_data_list))

                # 마지막으로 읽은 위치를 업데이트
                if file_name == "filtered_span.json":
                    # 파일 포인터를 마지막 읽은 위치로 이동
                    filter_last_position = log_file.tell()+2  # 현재 파일 포인터의 위치를 저장

                else:
                    original_last_position = log_file.tell()+2  # 현재 파일 포인터의 위치를 저장

                logging.info("============ trace 파싱 end ===========\n")
                logging.info(parsing_trace_data_list)

                return parsing_trace_data_list

    def redis_insert(self):

        file_name = self.file_name

        logging.info("============ db 삽입 start===========\n")

        # Redis 클라이언트 설정
        r = redis.Redis(host='100.83.227.59', port=16379, db=1, password='redis1234!')

        parsing_trace_data_list = self.traceparser()

        logging.info("**************************")
        logging.info("parsing_trace_data_list\n")
        logging.info(parsing_trace_data_list)
        logging.info("**************************")        #
        # for log in parsing_trace_data_list:
        #     trace_id = log['traceId']
        #
        #     # redis에 저장할 key 값 설정
        #     key_store_key = f"key_store:{trace_id}"
        #
        #     if file_name == "filtered_span.json":
        #         # 해시 키는 traceId로 설정
        #         hash_key = f"filtered_trace_hash:{trace_id}"
        #
        #     else:
        #         # 해시 키는 traceId로 설정
        #         hash_key = f"original_trace_hash:{trace_id}"
        #
        #     # # 현재 데이터를 JSON 형식으로 변환
        #     # log_json = json.dumps(log)
        #
        #     # parsing_data_log 필드가 존재하는지 확인하고, 없으면 리스트로 초기화
        #     existing_logs = r.hget(hash_key, 'parsing_data_trace')
        #     if existing_logs:
        #         existing_logs_list = json.loads(existing_logs)
        #     else:
        #         existing_logs_list = []
        #
        #     # 새로운 로그를 리스트에 추가
        #     existing_logs_list.append(log)
        #     logging.info("existing_logs")
        #     logging.info(existing_logs_list)
        #     # Redis에 업데이트된 리스트 저장 (HSET으로 해시 업데이트)
        #     r.hset(hash_key, "parsing_data_trace", json.dumps(existing_logs_list))
        #     r.hset(key_store_key, "retry", "0")
        #
        # # Redis에 저장된 데이터 확인 (예시)
        # for log in parsing_trace_data_list:
        #
        #     trace_id = log['traceId']
        #
        #     if file_name == "filtered_span.json":
        #         # 해시 키는 traceId로 설정
        #         hash_key = f"filtered_trace_hash:{trace_id}"
        #
        #     else:
        #         # 해시 키는 traceId로 설정
        #         hash_key = f"original_trace_hash:{trace_id}"
        #
        #     logging.info(f"Redis Key: {hash_key}")
        #     logging.info(r.hget(hash_key, "parsing_data_trace"))
        #     logging.info(r.hget(hash_key, "parsing_data_trace").decode("utf-8"))
        #
        #     logging.info("============ db 삽입 end===========\n")