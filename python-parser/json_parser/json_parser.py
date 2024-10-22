import json
import time
from datetime_util import change_timenano_format
import os

# 경로 설정
# log_file_name = "filtered_logs.json"
# span_file_name = "filtered_span.json"

log_file_name = "original_logs.json"
span_file_name = "original_span.json"

folder_name = "241022_scheduler_all"


log_file_path = "../../data" +"/"+ folder_name+"/" + log_file_name
span_file_path = "../../data" +"/"+ folder_name+"/" + span_file_name
output_path = "../../data" +"/"+ folder_name+"/" + 'output/'

log_file_name_one_row = 'one_row_' + log_file_name
log_file_name_multi_row = 'multi_row_' + log_file_name

span_file_name_one_row = 'one_row_' + span_file_name
span_file_name_multi_row = 'multi_row_' + span_file_name

# 경로에 폴더가 없으면 생성
if not os.path.exists(output_path):
    os.makedirs(output_path)

# 로그 데이터 파싱 및 필요한 key 값 추출
filtered_logs = []

# # traceId 값을 중복없이 저장하기 위해 빈 집합 초기화
# trace_ids = set()

with open(log_file_path, "r") as log_file:
    for line in log_file:
        try:
            log_data = json.loads(line.strip())
            change_timenano_format(log_data)  # 시간 전처리 적용

            for resource_log in log_data.get('resourceLogs', []):
                # scopeLogs와 logRecords에서 필요한 정보 추출
                for scope_log in resource_log.get("scopeLogs", []):
                    for log_record in scope_log.get("logRecords", []):
                        parsed_log = {
                            "container.id": None,
                            "os.description": None,
                            "process.command_line": None,
                            "service.name": None,
                            "service.code": None,
                            "telemetry.sdk.language": None,
                            "scope": None,
                            "logRecords_severityText": None,
                            "logRecords_body_stringValue": None,
                            "log.exception.message": None,
                            "log.exception.stacktrace": None,
                            "log.exception.stacktrace.short": None,
                            "log.exception.type": None,
                            "traceId": None,
                            "observedTimeUnixNano": None,  # 새로운 시간 필드 추가
                        }

                        # resource 부분에서 필요한 정보 추출
                        if "resource" in resource_log and "attributes" in resource_log["resource"]:
                            for attribute in resource_log["resource"]["attributes"]:
                                if attribute["key"] == "container.id":
                                    parsed_log["container.id"] = attribute["value"]["stringValue"]
                                if attribute["key"] == "os.description":
                                    parsed_log["os.description"] = attribute["value"]["stringValue"]
                                if attribute["key"] == "process.command_line":
                                    parsed_log["process.command_line"] = attribute["value"]["stringValue"]
                                if attribute["key"] == "service.name":
                                    parsed_log["service.name"] = attribute["value"]["stringValue"]
                                if attribute["key"] == "service.code":
                                    parsed_log["service.code"] = attribute["value"]["stringValue"]
                                if attribute["key"] == "telemetry.sdk.language":
                                    parsed_log["telemetry.sdk.language"] = attribute["value"]["stringValue"]
                        if "scope" in scope_log:
                            parsed_log["scope"] = scope_log["scope"]["name"]
                        if "observedTimeUnixNano" in log_record:
                            parsed_log["observedTimeUnixNano"] = log_record["observedTimeUnixNano"]
                        if "severityText" in log_record:
                            parsed_log["logRecords_severityText"] = log_record["severityText"]
                        if "body" in log_record and "stringValue" in log_record["body"]:
                            parsed_log["logRecords_body_stringValue"] = log_record["body"]["stringValue"]
                        if "attributes" in log_record:
                            for attribute in log_record["attributes"]:
                                if attribute["key"] == "exception.message":
                                    parsed_log["log.exception.message"] = attribute["value"]["stringValue"].replace(
                                        '"', '')
                                if attribute["key"] == "exception.stacktrace":
                                    parsed_log["log.exception.stacktrace"] = attribute["value"]["stringValue"].replace(
                                        '"', '')
                                    parsed_log["log.exception.stacktrace.short"] = ' '.join(line.strip() for line in
                                                                                                                        '')
                                if attribute["key"] == "exception.type":
                                    parsed_log["log.exception.type"] = attribute["value"]["stringValue"].replace('"',
                                                                                                                  '')
                        if "traceId" in log_record and log_record["traceId"] != "":
                            parsed_log["traceId"] = log_record["traceId"]
                            # trace_ids.add(log_record["traceId"])
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

# 로그 파싱 후 1초 딜레이
time.sleep(1)

# 스팬 데이터 파싱 및 필요한 key 값 추출
filtered_spans = []

with open(span_file_path, "r") as span_file:
    for line in span_file:
        try:
            span_data = json.loads(line.strip())
            change_timenano_format(span_data)  # 시간 전처리 적용

            for resourceSpan in span_data.get('resourceSpans', []):
                service_name = None
                service_code = None
                os_type = None

                if "resource" in resourceSpan and "attributes" in resourceSpan["resource"]:
                    for attribute in resourceSpan["resource"]["attributes"]:
                        if attribute["key"] == "service.name":
                            service_name = attribute["value"]["stringValue"]
                        if attribute["key"] == "service.code":
                            service_code = attribute["value"]["stringValue"]
                        if attribute["key"] == "os.type":
                            os_type = attribute["value"]["stringValue"]

                for scopeSpan in resourceSpan.get("scopeSpans", []):
                    for span in scopeSpan.get("spans", []):
                        # if span.get("traceId") in trace_ids:
                            parsed_info = {
                                "service.name": service_name,
                                "service.code": service_code,
                                "os.type": os_type,
                                "traceId": span.get("traceId"),
                                "spanId": span.get("spanId"),
                                "name": span.get("name"),
                                "http.status_code": None,
                                "http.response.status_code": None,
                                "server.address": None,
                                "server.port": None,
                                "trace.exception.message": None,
                                "trace.exception.stacktrace": None,
                                "trace.exception.stacktrace.short": None,
                                "trace.exception.type": None,
                                "http.url": None,
                                "http.route": None,
                                "rpc.method": None,
                                "startTimeUnixNano": span.get("startTimeUnixNano"),
                                "endTimeUnixNano": span.get("endTimeUnixNano")
                            }

                            for attribute in span.get("attributes", []):
                                if attribute["key"] == "http.status_code" and "intValue" in attribute["value"]:
                                    parsed_info["http.status_code"] = attribute["value"]["intValue"]
                                if attribute["key"] == "http.response.status_code" and "intValue" in attribute["value"]:
                                    parsed_info["http.response.status_code"] = attribute["value"]["intValue"]
                                if attribute["key"] == "rpc.grpc.status_code":
                                    parsed_info["rpc.grpc.status_code"] = attribute["value"]["intValue"]
                                if attribute["key"] == "server.address":
                                    parsed_info["server.address"] = attribute["value"]["stringValue"]
                                if attribute["key"] == "server.port":
                                    parsed_info["server.port"] = attribute["value"]["intValue"]
                                if attribute["key"] == "http.url":
                                    parsed_info["http.url"] = attribute["value"]["stringValue"]
                                if attribute["key"] == "http.route":
                                    parsed_info["http.url"] = attribute["value"]["stringValue"]
                                if attribute["key"] == "rpc.method":
                                    parsed_info["rpc.method"] = attribute["value"]["stringValue"]

                            for event in span.get("events", []):
                                for attribute in event.get("attributes", []):
                                    if attribute["key"] == "exception.message":
                                        parsed_info["trace.exception.message"] = attribute["value"]["stringValue"].replace('"', '')
                                    if attribute["key"] == "exception.stacktrace":
                                        parsed_info["trace.exception.stacktrace"] = attribute["value"]["stringValue"].replace('"', '')
                                        parsed_info["trace.exception.stacktrace.short"] = ' '.join(
                                            line.strip() for line in attribute["value"]["stringValue"].split('\n')[:2]).replace('"', '')
                                    if attribute["key"] == "exception.type":
                                        parsed_info["trace.exception.type"] = attribute["value"]["stringValue"].replace('"', '')

                            filtered_spans.append(parsed_info)

        except json.JSONDecodeError as e:
            print(f"Error parsing line: {e}")


# 스팬 데이터를 파일에 저장 (한 줄)
with open(output_path + span_file_name_one_row, 'w') as span_output_file:
    json.dump(filtered_spans, span_output_file, separators=(',', ':'))

# 스팬 데이터를 파일에 저장 (여러 줄)
with open(output_path + span_file_name_multi_row, 'w') as span_output_file:
    json.dump(filtered_spans, span_output_file, indent=4)

# 결과 출력 (확인용)
print("에러가 발생한 스팬입니다.")
print(json.dumps(filtered_spans, indent=4))

