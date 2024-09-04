import json
import time
from datetime_util import change_timenano_format

# 경로 설정
log_file_path = "./data/paymentServiceFailure/original_logs.json"
output_path = './data/paymentServiceFailure/output/'
log_file_name_one_row = 'original_logs.json'
log_file_name_multi_row = 'pretty_original_logs.json'

# 로그 데이터 파싱 및 필요한 key 값 추출
filtered_logs = []

# traceId 값을 중복없이 저장하기 위해 빈 집합 초기화
trace_ids = set()

with open(log_file_path, "r") as log_file:
    for line in log_file:
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
                for scope_log in resource_log.get("scopeLogs", []):
                    for log_record in scope_log.get("logRecords", []):
                        if "observedTimeUnixNano" in log_record:
                            parsed_log["observedTimeUnixNano"] = log_record["observedTimeUnixNano"]
                        if "severityText" in log_record:
                            parsed_log["logRecords_severityText"] = log_record["severityText"]
                        if "body" in log_record and "stringValue" in log_record["body"]:
                            parsed_log["logRecords_body_stringValue"] = log_record["body"]["stringValue"]
                        if "traceId" in log_record and log_record["traceId"] != "":
                            parsed_log["traceId"] = log_record["traceId"]
                            trace_ids.add(log_record["traceId"])
                            # traceId가 유효한 경우에만 logRecord 추가
                            filtered_logs.append(parsed_log)

        except json.JSONDecodeError as e:
            print(f"Error parsing line: {e}")

# 로그 데이터를 파일에 저장 (한 줄)
with open(output_path + log_file_name_one_row, 'w') as log_output_file:
    json.dump(filtered_logs, log_output_file, separators=(',', ':'))

# 스팬 데이터를 파일에 저장 (여러 줄)
with open(output_path + log_file_name_multi_row, 'w') as log_output_file:
    json.dump(filtered_logs, log_output_file, indent=4)

# 결과 출력 (확인용)
print("에러가 발생한 로그입니다.")
print(json.dumps(filtered_logs, indent=4))