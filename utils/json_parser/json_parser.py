import json
from datetime import datetime, timezone
import pytz

# 경로 설정
json_file_path = "./data/adServiceFailure/filtered_span.json"
output_file_path = './data/adServiceFailure/output/filtered_span.json'

# JSON 파일을 읽어오기
json_data = []
with open(json_file_path, "r") as json_file:
    for line in json_file:
        try:
            data = json.loads(line.strip())
            json_data.append(data)
        except json.JSONDecodeError as e:
            print(f"Error parsing line: {e}")

# 나노초를 datetime으로 변환하는 함수
def convert_nano_to_datetime(nano_time):
    # 나노초를 초로 변환
    seconds = nano_time // 1000000000
    # 초를 UTC 시간대로 변환
    utc_dt = datetime.fromtimestamp(seconds, tz=timezone.utc)
    # UTC 시간대를 한국 시간대로 변환
    kst_tz = pytz.timezone('Asia/Seoul')
    kst_dt = utc_dt.astimezone(kst_tz)
    # 원하는 형식으로 포맷 맞추기
    return kst_dt.strftime('%Y-%m-%d %H:%M:%S')

# json의 timenano 키의 값을 datetime으로 변환하는 함수. 재귀적으로 key를 찾음
def change_timenano_format(first_json):
    if isinstance(first_json, dict):
        for k, v in first_json.items():
            if k in ["timeUnixNano", "startTimeUnixNano", "observedTimeUnixNano", "endTimeUnixNano"]:
                formatted_time = convert_nano_to_datetime(int(v))
                first_json[k] = formatted_time
            else:
                change_timenano_format(v)
    elif isinstance(first_json, list):
        for item in first_json:
            change_timenano_format(item)
    else:
        return

# trace_id가 특정 값일 때만 작업 수행
trace_id_to_check = "a3068c5690d7e955872ea04eb2f2859b"
filtered_json_data = []

# JSON 데이터 파싱 및 필요한 key 값 추출
for item in json_data:
    change_timenano_format(item)  # 시간 전처리 적용
    for resourceSpan in item.get('resourceSpans', []):
        service_name = None
        os_type = None
        # service.name 및 os.type 추출
        if "resource" in resourceSpan and "attributes" in resourceSpan["resource"]:
            for attribute in resourceSpan["resource"]["attributes"]:
                if attribute["key"] == "service.name":
                    service_name = attribute["value"]["stringValue"]
                if attribute["key"] == "os.type":
                    os_type = attribute["value"]["stringValue"]

        # scopeSpans 추출 및 필터링
        for scopeSpan in resourceSpan.get("scopeSpans", []):
            for span in scopeSpan.get("spans", []):
                if span.get("traceId") == trace_id_to_check:
                    parsed_info = {
                        "service.name": service_name,
                        "os.type": os_type,
                        "traceId": span.get("traceId"),
                        "spanId": span.get("spanId"),
                        "name": span.get("name"),
                        "http.status_code": None,
                        "rpc.grpc.status_code": None,
                        "exception.message": None,
                        "exception.stacktrace": None,
                        "http.url": None,
                        "rpc.method": None,
                        "startTimeUnixNano": span.get("startTimeUnixNano"),
                        "endTimeUnixNano": span.get("endTimeUnixNano")
                    }

                    # span의 attributes를 추출
                    for attribute in span.get("attributes", []):
                        if attribute["key"] == "http.status_code":
                            parsed_info["http.status_code"] = attribute["value"]["intValue"]
                        elif attribute["key"] == "rpc.grpc.status_code":
                            parsed_info["rpc.grpc.status_code"] = attribute["value"]["intValue"]
                        elif attribute["key"] == "http.url":
                            parsed_info["http.url"] = attribute["value"]["stringValue"]
                        elif attribute["key"] == "rpc.method":
                            parsed_info["rpc.method"] = attribute["value"]["stringValue"]

                    # events의 attributes에서 exception.message와 exception.stacktrace 추출
                    for event in span.get("events", []):
                        for attribute in event.get("attributes", []):
                            if attribute["key"] == "exception.message":
                                parsed_info["exception.message"] = attribute["value"]["stringValue"]
                            elif attribute["key"] == "exception.stacktrace":
                                parsed_info["exception.stacktrace"] = attribute["value"]["stringValue"]

                    filtered_json_data.append(parsed_info)

# 결과 출력 (확인용)
for result in filtered_json_data:
    print(json.dumps(result, indent=4))

# 결과를 한 줄로 출력
json_output = json.dumps(filtered_json_data, separators=(',', ':'))

# 결과 출력 (확인용)
print(json_output)

# 필요한 key 값만 포함된 데이터를 저장
with open(output_file_path, 'w') as f:
    f.write(json_output)

# # 필요한 key 값만 포함된 데이터를 저장
# with open(output_file_path, 'w') as f:
#     json.dump(filtered_json_data, f, indent=4)  # indent=4는 읽기 쉽게 들여쓰기를 추가합니다.
