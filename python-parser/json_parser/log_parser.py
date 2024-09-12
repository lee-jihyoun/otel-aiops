import json, itertools
from util.datetime_util import change_timenano_format
import variables.trace_id as trace_id

# 로그 데이터 파싱 및 필요한 key 값 추출
# JSON 파일을 읽어오기
# 2개는 trace_id_dict.json에 있고 2개는 trace_id_dict.json에 존재하지 않음
# 존재하지 않을 경우 trace_id_dict.json에 추가하기

# trace_id_dict 테스트용
trace_id.trace_id_dict["log_parser"] = ""


class LogParsing:

    def __init__(self, input_path, output_path, idx, file_name):

        self.input_path = input_path
        self.output_path = output_path
        self.file_name = file_name
        self.idx = idx

    # def get_trace_status_entries(self, trace_id_dict):
    #     print("trace_id_dict: ", trace_id_dict)
    #     return {key: value for key, value in trace_id_dict.items() if value.get("status") == "trace"}

    def logparser(self):
        filtered_logs = []
        flag = 0

        input_path = self.input_path
        output_path = self.output_path
        file_name = self.file_name
        idx = self.idx

        trace_id_dict = trace_id.trace_id_dict

        existing_trace_ids_dict = trace_id_dict
        print("existing_trace_ids_dict: ", existing_trace_ids_dict) # Trace_id_dict 불러와서 저장

        with open(input_path + file_name, "r") as log_file:
            for current_index, line in enumerate(itertools.islice(log_file, idx, None), start=idx):
                print(line.strip())
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

                        # resource 부분에서 필요한 정보 추출
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

                        # scopeLogs와 logRecords에서 필요한 정보 추출
                        # observedTimeUnixNano, severityText, body, traceId
                        # traceId가 유효한 경우에만 logRecord 추가
                        for scope_log in resource_log.get("scopeLogs", []):
                            for log_record in scope_log.get("logRecords", []):
                                if "observedTimeUnixNano" in log_record:
                                    parsed_log["observedTimeUnixNano"] = log_record["observedTimeUnixNano"]
                                if "severityText" in log_record:
                                    parsed_log["logRecords_severityText"] = log_record["severityText"]
                                if "body" in log_record and "stringValue" in log_record["body"]:
                                    parsed_log["logRecords_body_stringValue"] = log_record["body"]["stringValue"]

                                print("222222222222")
                                print(trace_id_dict)

                                # 상태가 trace인가?
                                trace_status_entries = {key: value for key, value in trace_id_dict.items() if
                                                        isinstance(value, dict) and value.get('status') == 'trace'}
                                print(trace_status_entries)

                                # trace_id_dict에 상태값이 trace인가 (trace_status_entries 내에 trace_id_dict가 존재하는가) (Y)
                                if len(trace_status_entries) > 0:

                                    # 파싱된 로그와 딕셔너리에 있는 trace ID값이 일치 하는가 (Y)
                                    if log_record["traceId"] in trace_status_entries:
                                        parsed_log["traceId"] = log_record["traceId"]
                                        trace_id_dict[log_record["traceId"]]["status"] = "true"
                                        filtered_logs.append(parsed_log)

                                    else:
                                        pass

                                # trace_id_dict에 상태값이 trace인가 (N)
                                else:
                                    # 파싱된 로그에 trace ID가 있는가? (Y)
                                    if "traceId" in log_record and log_record["traceId"] != "":
                                        # trace_id_dict에 key가 있는가? (N)
                                        if log_record["traceId"] not in trace_id_dict:
                                            parsed_log["traceId"] = log_record["traceId"]
                                            trace_id_dict[log_record["traceId"]] = {"status": "log",
                                                                                    "retry": 0,
                                                                                    "mail": "N"}
                                            filtered_logs.append(parsed_log)

                                        # trace_id_dict에 key가 있는가? (Y)
                                        else:
                                            pass

                                    # 파싱된 로그에 trace ID가 있는가? (N)
                                    else:
                                        pass

                                # # id 비교하는거
                                # if "traceId" in log_record and log_record["traceId"] != "" and log_record["traceId"] not in trace_id_dict:
                                #     parsed_log["traceId"] = log_record["traceId"]
                                #
                                #     print("11111111111111111111111111")
                                #     print(log_record["traceId"])
                                #     print(trace_id_dict)
                                #
                                #     trace_id_dict[log_record["traceId"]] = {"status": "log",
                                #                                             "retry": 0,
                                #                                             "mail": "N"}
                                #
                                #     # traceId가 유효한 경우에만 logRecord 추가
                                #     filtered_logs.append(parsed_log)

                except json.JSONDecodeError as e:
                    print(f"Error parsing line: {e}")


        # 로그 데이터를 파일에 저장 (한 줄)
        with open(output_path + 'one_row_' + file_name, 'w', encoding='utf-8') as log_output_file:
            json.dump(filtered_logs, log_output_file, separators=(',', ':'))

        # 스팬 데이터를 파일에 저장 (여러 줄)
        with open(output_path + 'multi_row_' + file_name, 'w', encoding='utf-8') as log_output_file:
            json.dump(filtered_logs, log_output_file, indent=4)
        print("new_idx: ", idx)
        # 새로운 인덱스, filtered logs, flag 값 리턴
        return idx, filtered_logs

    def original_logparser(self):
        original_logs = []

        input_path = self.input_path
        output_path = self.output_path
        file_name = self.file_name
        idx = self.idx

        trace_id_dict = trace_id.trace_id_dict

        existing_trace_ids_dict = trace_id_dict
        print("existing_trace_ids_dict: ", existing_trace_ids_dict)  # Trace_id_dict 불러와서 저장

        with open(input_path + file_name, "r") as log_file:
            for current_index, line in enumerate(itertools.islice(log_file, idx, None), start=idx):
                print(line.strip())
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

                        # resource 부분에서 필요한 정보 추출
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

                        # scopeLogs와 logRecords에서 필요한 정보 추출
                        # observedTimeUnixNano, severityText, body, traceId
                        # traceId가 유효한 경우에만 logRecord 추가
                        for scope_log in resource_log.get("scopeLogs", []):
                            for log_record in scope_log.get("logRecords", []):
                                if "observedTimeUnixNano" in log_record:
                                    parsed_log["observedTimeUnixNano"] = log_record["observedTimeUnixNano"]
                                if "severityText" in log_record:
                                    parsed_log["logRecords_severityText"] = log_record["severityText"]
                                if "body" in log_record and "stringValue" in log_record["body"]:
                                    parsed_log["logRecords_body_stringValue"] = log_record["body"]["stringValue"]

                                print("222222222222")
                                print(trace_id_dict)

                                # 상태가 trace인가?
                                trace_status_entries = {key: value for key, value in trace_id_dict.items() if
                                                        isinstance(value, dict) and value.get('status') == 'trace'}
                                print(trace_status_entries)

                                # trace_id_dict에 상태값이 trace인가 (trace_status_entries 내에 trace_id_dict가 존재하는가) (Y)
                                if len(trace_status_entries) > 0:

                                    # 원문로그에 해당 trace id 가 있는가 (Y)
                                    if log_record["traceId"] in trace_status_entries:
                                        parsed_log["traceId"] = log_record["traceId"]
                                        trace_id_dict[log_record["traceId"]]["status"] = "true"
                                        original_logs.append(parsed_log)

                                    else:
                                        # trace_id_dict에 있는 해당 키의 리트라이 횟수가 3 미만인가
                                        if trace_id_dict[log_record["traceId"]]["retry"] < 3:
                                            # 리트라이 횟수 증가
                                            trace_id_dict[log_record["traceId"]]["retry"] += 1
                                            # 로그에 추가
                                            original_logs.append(parsed_log)

                                        else:
                                            parsed_log["traceId"] = log_record["traceId"]
                                            trace_id_dict[log_record["traceId"]]["status"] = "true"

                except json.JSONDecodeError as e:
                    print(f"Error parsing line: {e}")

        # 로그 데이터를 파일에 저장 (한 줄)
        with open(output_path + 'one_row_' + file_name, 'w', encoding='utf-8') as log_output_file:
            json.dump(original_logs, log_output_file, separators=(',', ':'))

        # 스팬 데이터를 파일에 저장 (여러 줄)
        with open(output_path + 'multi_row_' + file_name, 'w', encoding='utf-8') as log_output_file:
            json.dump(original_logs, log_output_file, indent=4)
        print("new_idx: ", idx)
        # 새로운 인덱스, filtered logs 값 리턴
        return idx, original_logs