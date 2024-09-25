import json, itertools, datetime
from util.datetime_util import change_timenano_format
import logging, redis


class LogParsing:

    def __init__(self, input_path, file_name):

        self.input_path = input_path
        self.file_name = file_name

    def logparser(self):
        input_path = self.input_path
        file_name = self.file_name

        print("인덱스 초기화")
        last_index = 0
        while True:
            parsing_log_data_list = []

            print("-=-=-=-=-----------start-=-=----------")

            with open(input_path + file_name, "r") as log_file:
                print("-=-=-=-=-----------for문 시작-=-=----------")
                print(log_file)
                for current_index, line in enumerate(itertools.islice(log_file, None), start=100):

                    # 디버깅할 때 사용..
                    print('* 아무 글자나 입력:', current_index, last_index, line)
                    input()
                    last_index = current_index + 1

                    logging.info(f"================ filtered_log 파싱 start: {datetime.datetime.now()} ================")

                    try:
                        log_data = json.loads(line.strip())
                        change_timenano_format(log_data)  # 시간 전처리 적용
                        for resource_log in log_data.get('resourceLogs', []):
                            for scope_log in resource_log.get("scopeLogs", []):
                                for log_record in scope_log.get("logRecords", []):
                                    parsed_info = {
                                        "container.id": None,
                                        "os.description": None,
                                        "process.command_line": None,
                                        "service.name": None,
                                        "service.code": None,
                                        "telemetry.sdk.language": None,
                                        "logRecords_severityText": None,
                                        "logRecords_body_stringValue": None,
                                        "traceId": None,
                                        "observedTimeUnixNano": None,  # 새로운 시간 필드 추가
                                    }
                                    if "resource" in resource_log and "attributes" in resource_log["resource"]:
                                        for attribute in resource_log["resource"]["attributes"]:
                                            if attribute["key"] == "container.id":
                                                parsed_info["container.id"] = attribute["value"]["stringValue"]
                                            if attribute["key"] == "os.description":
                                                parsed_info["os.description"] = attribute["value"]["stringValue"]
                                            if attribute["key"] == "process.command_line":
                                                parsed_info["process.command_line"] = attribute["value"]["stringValue"]
                                            if attribute["key"] == "service.name":
                                                parsed_info["service.name"] = attribute["value"]["stringValue"]
                                            if attribute["key"] == "service.code":
                                                parsed_info["service.code"] = attribute["value"]["stringValue"]
                                            if attribute["key"] == "telemetry.sdk.language":
                                                parsed_info["telemetry.sdk.language"] = attribute["value"]["stringValue"]

                                    if "observedTimeUnixNano" in log_record:
                                        parsed_info["observedTimeUnixNano"] = log_record["observedTimeUnixNano"]
                                    if "severityText" in log_record:
                                        parsed_info["logRecords_severityText"] = log_record["severityText"]
                                    if "body" in log_record and "stringValue" in log_record["body"]:
                                        parsed_info["logRecords_body_stringValue"] = log_record["body"]["stringValue"]
                                    if "traceId" in log_record:
                                        parsed_info["traceId"] = log_record["traceId"]
                                        print(parsed_info)

                                    # traceid가 비어 있을 경우에는 log_record에 저장하지 않음
                                    if "traceId" in log_record and log_record["traceId"]:
                                        parsing_log_data_list.append(parsed_info)

                    # idx = current_index + 1
                    # print(idx)
                    #
                    # logging.info(f"* idx: {idx}")

                    except json.JSONDecodeError as e:
                        logging.ERROR(f"Error parsing line: {e}")

                logging.info("============ log 파싱 end ===========\n")
                print(parsing_log_data_list)

                logging.info("============ db 삽입 start===========\n")

                # Redis 클라이언트 설정
                r = redis.Redis(host='100.83.227.59', port=16379, db=1, password='redis1234!')

                for log in parsing_log_data_list:
                    trace_id = log['traceId']

                    if file_name == "filtered_logs.json":
                        # 해시 키는 traceId로 설정
                        hash_key = f"filtered_log_hash:{trace_id}"

                    else:
                        # 해시 키는 traceId로 설정
                        hash_key = f"original_log_hash:{trace_id}"

                    # # 현재 데이터를 JSON 형식으로 변환
                    # log_json = json.dumps(log)

                    # parsing_data_log 필드가 존재하는지 확인하고, 없으면 리스트로 초기화
                    existing_logs = r.hget(hash_key, 'parsing_data_log')
                    if existing_logs:
                        existing_logs_list = json.loads(existing_logs)
                    else:
                        existing_logs_list = []

                    # 새로운 로그를 리스트에 추가
                    existing_logs_list.append(log)
                    print("existing_logs")
                    print(existing_logs_list)
                    # Redis에 업데이트된 리스트 저장 (HSET으로 해시 업데이트)
                    r.hset(hash_key, "parsing_data_log", json.dumps(existing_logs_list))

                # Redis에 저장된 데이터 확인 (예시)
                for log in parsing_log_data_list:
                    trace_id = log['traceId']
                    hash_key = f"filtered_log_hash:{trace_id}"
                    print(f"Redis Key: {hash_key}")
                    print(r.hget(hash_key, "parsing_data_log").decode("utf-8"))

                    logging.info("============ db 삽입 end===========\n")