import json, itertools, datetime
from util.datetime_util import change_timenano_format
import variables.trace_id as trace_id
import variables.file_idx as file_idx
import logging, redis


class LogParsing:

    def __init__(self, input_path, file_name, file_idx):

        self.input_path = input_path
        self.file_name = file_name
        self.idx = file_idx

    def logparser(self):
        input_path = self.input_path
        file_name = self.file_name
        idx = self.idx

        # # Redis 클라이언트 설정
        # r = redis.Redis(host='100.83.227.59', port=16379, db=0, password='redis1234!')

        parsing_log_data_list = []

        with open(input_path + file_name, "r") as log_file:
            for current_index, line in enumerate(itertools.islice(log_file, idx, None), start=idx):

                # 디버깅할 때 사용..
                print('* 아무 글자나 입력:')
                input()

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
                                parsing_log_data_list.append(parsed_info)

                except json.JSONDecodeError as e:
                    logging.ERROR(f"Error parsing line: {e}")

                logging.info("============ filtered log 파싱 end ===========\n")

                print(parsing_log_data_list)
                file_idx.idx["logs"] = current_index + 1
                logging.info(f"* idx: {current_index}")