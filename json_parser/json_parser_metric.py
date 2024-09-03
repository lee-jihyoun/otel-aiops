import json
import time
from datetime import datetime, timezone
import pytz

# JSON 파일 경로 설정
json_file_path = "./data/adServiceHighCpu/original_metrics.json"
output_path = "./data/adServiceHighCpu/output/"
output_file_path = "./data/adServiceHighCpu/output/original_metrics.json"

# 나노초를 datetime으로 변환하는 함수
def convert_nano_to_datetime(nano_time):
    seconds = nano_time // 1000000000
    utc_dt = datetime.fromtimestamp(seconds, tz=timezone.utc)
    kst_tz = pytz.timezone('Asia/Seoul')
    kst_dt = utc_dt.astimezone(kst_tz)
    return kst_dt.strftime('%Y-%m-%d %H:%M:%S')

# json의 timenano 키의 값을 datetime으로 변환하는 함수. 재귀적으로 key를 찾음
def change_timenano_format(first_json):
    if isinstance(first_json, dict):
        for k, v in first_json.items():
            if k in ["timeUnixNano", "startTimeUnixNano", "observedTimeUnixNano", "endTimeUnixNano"]:
                if isinstance(v, (int, str)) and v.isdigit():  # Check if v is a digit and not already formatted
                    formatted_time = convert_nano_to_datetime(int(v))
                    first_json[k] = formatted_time
            else:
                change_timenano_format(v)
    elif isinstance(first_json, list):
        for item in first_json:
            change_timenano_format(item)
    else:
        return


# 메트릭 파싱 함수 정의
def parse_metrics(file_path, metric_names):
    filtered_metrics = []

    with open(file_path, "r") as json_file:
        for line in json_file:
            try:
                data = json.loads(line.strip())
                change_timenano_format(data)
                for resource_metric in data.get("resourceMetrics", []):
                    for scope_metric in resource_metric.get("scopeMetrics", []):
                        for metric in scope_metric.get("metrics", []):
                            if metric.get("name") in metric_names:
                                value_key = "asDouble" if metric.get(
                                    "name") != "process.runtime.cpython.memory" else "asInt"
                                for data_point in metric.get("sum", {}).get("dataPoints", []):
                                    metric_info = {
                                        "metric_name": metric.get("name"),
                                        "type": None,
                                        "startTimeUnixNano": data_point.get("startTimeUnixNano"),
                                        "timeUnixNano": data_point.get("timeUnixNano"),
                                        "value": data_point.get(value_key)
                                    }
                                    for attribute in data_point.get("attributes", []):
                                        if attribute.get("key") == "type":
                                            metric_info["type"] = attribute.get("value", {}).get("stringValue")
                                    filtered_metrics.append(metric_info)
                                for data_point in metric.get("gauge", {}).get("dataPoints", []):
                                    metric_info = {
                                        "metric_name": metric.get("name"),
                                        "type": None,
                                        "startTimeUnixNano": data_point.get("startTimeUnixNano"),
                                        "timeUnixNano": data_point.get("timeUnixNano"),
                                        "value": data_point.get(value_key)
                                    }
                                    for attribute in data_point.get("attributes", []):
                                        if attribute.get("key") == "type":
                                            metric_info["type"] = attribute.get("value", {}).get("stringValue")
                                    filtered_metrics.append(metric_info)
            except json.JSONDecodeError as e:
                print(f"Error parsing line: {e}")

    return filtered_metrics


# 파싱할 메트릭 키 리스트
metric_keys = [
    "process.runtime.cpython.cpu_time",
    "process.runtime.cpython.memory",
    "process.runtime.cpython.cpu.utilization"
]

# 메트릭 파싱 및 출력
parsed_metrics = parse_metrics(json_file_path, metric_keys)

# 메트릭 데이터를 파일에 저장 (한 줄)
with open(output_path + 'original_metrics.json', 'w') as metric_output_file:
    json.dump(parsed_metrics, metric_output_file, separators=(',', ':'))

# 스팬 데이터를 파일에 저장 (여러 줄)
with open(output_path + 'pretty_original_metrics.json', 'w') as metric_output_file:
    json.dump(parsed_metrics, metric_output_file, indent=4)

# 결과 출력 (확인용)
print("파싱된 메트릭 데이터입니다:")
print(json.dumps(parsed_metrics, indent=4))