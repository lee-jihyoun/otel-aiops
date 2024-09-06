import json, itertools
from util.datetime_util import change_timenano_format

# 로그 데이터 파싱 및 필요한 key 값 추출
# JSON 파일을 읽어오기
# 2개는 trace_id_dict.json에 있고 2개는 trace_id_dict.json에 존재하지 않음
# 존재하지 않을 경우 trace_id_dict.json에 추가하기

# 파일이 변경되었을 때 해당하는 인덱스로부터 읽어들어오기

class LogParsing:

    global trace_ids_dict

    def __init__(self, input_path, output_path, file_name, idx):
        self.input_path = input_path
        self.output_path = output_path
        self.file_name = file_name
        self.idx = idx

    def logparser(self):
        filtered_logs = []

        input_path = self.input_path
        output_path = self.output_path
        file_name = self.file_name
        idx = self.idx

        # global 변수로 수정하기
        existing_trace_ids_dict = trace_ids_dict.copy()

        with open(input_path + file_name, "r") as log_file:
            for line in itertools.islice(log_file, idx, None):  # 4번째 라인 이후부터 읽기
            #     print(line.strip())
            # for line in log_file:
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

                                # id 비교하는거
                                if "traceId" in log_record and log_record["traceId"] != "" and log_record["traceId"] not in trace_ids_dict:
                                    parsed_log["traceId"] = log_record["traceId"]

                                    trace_ids_dict[log_record["traceId"]] = ""

                                    # traceId가 유효한 경우에만 logRecord 추가
                                    filtered_logs.append(parsed_log)

                except json.JSONDecodeError as e:
                    print(f"Error parsing line: {e}")

        trace_ids = {key: value for key, value in trace_ids_dict.items()
                     if key not in existing_trace_ids_dict or existing_trace_ids_dict[key] != value}

        # 새로운 trace_id 저장
        with open(input_path + 'trace_id_dict.json', "w", encoding='utf-8') as trace_id_file:
            json.dump(trace_ids_dict, trace_id_file, indent=4)

        # 로그 데이터를 파일에 저장 (한 줄)
        with open(output_path + 'one_row_' + file_name, 'w', encoding='utf-8') as log_output_file:
            json.dump(filtered_logs, log_output_file, separators=(',', ':'))

        # 스팬 데이터를 파일에 저장 (여러 줄)
        with open(output_path + 'multi_row_' + file_name, 'w', encoding='utf-8') as log_output_file:
            json.dump(filtered_logs, log_output_file, indent=4)

        return idx, trace_ids, filtered_logs

        # 결과 출력 (확인용)
        # print("에러가 발생한 로그입니다.")
        # print(json.dumps(filtered_logs, indent=4))