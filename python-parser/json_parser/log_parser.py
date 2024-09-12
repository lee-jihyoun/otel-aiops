import json, itertools
from util.datetime_util import change_timenano_format
import variables.trace_id as trace_id

# 로그 데이터 파싱 및 필요한 key 값 추출
# JSON 파일을 읽어오기
# 2개는 trace_id_dict.json에 있고 2개는 trace_id_dict.json에 존재하지 않음
# 존재하지 않을 경우 trace_id_dict.json에 추가하기

# # trace_id_dict 테스트용
# trace_id.trace_id_dict["log_parser"] = ""


class LogParsing:

    def __init__(self, input_path, output_path, idx, file_name):

        self.input_path = input_path
        self.output_path = output_path
        self.file_name = file_name
        self.idx = idx

    def process_filtered_log(self, trace_id_dict, log_record, parsed_log, filtered_logs):
        # 상태가 trace인가?
        print("상태가 trace인가?\n")
        trace_status_entries = {key: value for key, value in trace_id_dict.items() if
                                isinstance(value, dict) and value.get('status') == 'trace'}
        print(trace_status_entries)

        # trace_id_dict에 상태값이 trace인가 (trace_status_entries 내에 trace_id_dict가 존재하는가) (Y)
        if len(trace_status_entries) > 0:
            print("trace_id_dict에 상태값이 trace인가 (trace_status_entries 내에 trace_id_dict가 존재하는가) (Y)\n")

            # 파싱된 로그와 딕셔너리에 있는 trace ID값이 일치 하는가 (Y)
            if log_record["traceId"] in trace_status_entries:
                print("파싱된 로그와 딕셔너리에 있는 trace ID값이 일치 하는가 (Y)\n")
                parsed_log["traceId"] = log_record["traceId"]
                trace_id_dict[log_record["traceId"]]["status"] = "true"
                filtered_logs.append(parsed_log)

            else:
                print("파싱된 로그와 딕셔너리에 있는 trace ID값이 일치 하는가 (N)\n")
                pass

        # trace_id_dict에 상태값이 trace인가 (N)
        else:
            print("trace_id_dict에 상태값이 trace인가 (N)\n")

            # 파싱된 로그에 trace ID가 있는가? (Y)
            if "traceId" in log_record and log_record["traceId"] != "":
                print("파싱된 로그에 trace ID가 있는가? (Y)\n")

                # trace_id_dict에 key가 있는가? (N)
                if log_record["traceId"] not in trace_id_dict:
                    print("trace_id_dict에 key가 있는가? (N)\n")
                    parsed_log["traceId"] = log_record["traceId"]
                    trace_id_dict[log_record["traceId"]] = {"status": "log",
                                                            "retry": 0,
                                                            "mail": "N"}
                    filtered_logs.append(parsed_log)

                # trace_id_dict에 key가 있는가? (Y)
                else:
                    print("# trace_id_dict에 key가 있는가? (Y)\n")
                    pass

            # 파싱된 로그에 trace ID가 있는가? (N)
            else:
                print("# 파싱된 로그에 trace ID가 있는가? (N)\n")
                pass

    def process_original_log(self, trace_id_dict, log_record, parsed_log, original_logs):
        # 상태가 trace인가?
        print("상태가 trace인가?\n")
        trace_status_entries = {key: value for key, value in trace_id_dict.items() if
                                isinstance(value, dict) and value.get('status') == 'trace'}
        print(trace_status_entries)

        # trace_id_dict에 상태값이 trace인가 (trace_status_entries 내에 trace_id_dict가 존재하는가) (Y)
        if len(trace_status_entries) > 0:
            print("trace_id_dict에 상태값이 trace인가 (trace_status_entries 내에 trace_id_dict가 존재하는가) (Y)\n")

            # 원문로그에 해당 trace id 가 있는가 (Y)
            if log_record["traceId"] in trace_status_entries:
                print("원문로그에 해당 trace id 가 있는가 (Y)\n")
                parsed_log["traceId"] = log_record["traceId"]
                trace_id_dict[log_record["traceId"]]["status"] = "true"
                original_logs.append(parsed_log)
            else:
                # trace_id_dict에 있는 해당 키의 리트라이 횟수가 3 미만인가
                print("trace_id_dict에 있는 해당 키의 리트라이 횟수가 3 미만인가 (Y)\n")
                # trace_status_entries에서 retry 값을 1씩 증가
                for trace_id, trace_info in trace_status_entries.items():
                    if trace_info.get("retry", 0) < 3:  # retry가 3 미만일 때만 증가
                        trace_info["retry"] += 1
                        print(f"Trace ID: {trace_id}, Retry 증가: {trace_info['retry']}")
                    else:
                        trace_info["status"] = 'true'
                        print(f"Trace ID: {trace_id}, Retry 횟수가 이미 3에 도달")

    def logparser(self):
        result = []

        input_path = self.input_path
        file_name = self.file_name
        idx = self.idx
        trace_id_dict = trace_id.trace_id_dict

        existing_trace_ids_dict = trace_id_dict
        print("existing_trace_ids_dict: ", existing_trace_ids_dict)  # Trace_id_dict 불러와서 저장

        with open(input_path + file_name, "r") as log_file:
            for current_index, line in enumerate(itertools.islice(log_file, idx, None), start=idx):
                try:
                    log_data = json.loads(line.strip())
                    change_timenano_format(log_data)  # 시간 전처리 적용

                    for resource_log in log_data.get('resourceLogs', []):
                        parsed_log = {
                            "container.id": None,
                            "os.description": None,
                            "process.command_line": None,
                            "service.name": None,
                            "telemetry.sdk.language": None,
                            "logRecords_severityText": None,
                            "logRecords_body_stringValue": None,
                            "traceId": None,
                            "observedTimeUnixNano": None,  # 새로운 시간 필드 추가
                        }

                        if "resource" in resource_log and "attributes" in resource_log["resource"]:
                            for attribute in resource_log["resource"]["attributes"]:
                                if attribute["key"] == "container.id":
                                    parsed_log["container.id"] = attribute["value"]["stringValue"]
                                elif attribute["key"] == "os.description":
                                    parsed_log["os.description"] = attribute["value"]["stringValue"]
                                elif attribute["key"] == "process.command_line":
                                    parsed_log["process.command_line"] = attribute["value"]["stringValue"]
                                elif attribute["key"] == "service.name":
                                    parsed_log["service.name"] = attribute["value"]["stringValue"]
                                elif attribute["key"] == "telemetry.sdk.language":
                                    parsed_log["telemetry.sdk.language"] = attribute["value"]["stringValue"]

                        for scope_log in resource_log.get("scopeLogs", []):
                            for log_record in scope_log.get("logRecords", []):
                                if "observedTimeUnixNano" in log_record:
                                    parsed_log["observedTimeUnixNano"] = log_record["observedTimeUnixNano"]
                                if "severityText" in log_record:
                                    parsed_log["logRecords_severityText"] = log_record["severityText"]
                                if "body" in log_record and "stringValue" in log_record["body"]:
                                    parsed_log["logRecords_body_stringValue"] = log_record["body"]["stringValue"]

                                if self.file_name == 'filtered_logs.json':
                                    self.process_filtered_log(trace_id_dict, log_record, parsed_log, result)

                                else:
                                    self.process_original_log(trace_id_dict, log_record, parsed_log, result)

                except json.JSONDecodeError as e:
                    print(f"Error parsing line: {e}")

        print("new_idx: ", idx)
        # 새로운 인덱스, filtered logs 값 리턴
        return idx, result