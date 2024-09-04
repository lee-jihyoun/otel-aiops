import json
from datetime import timedelta
from datetime_util import change_timenano_format, convert_string_to_datetime
# JSON 파일 경로 설정
json_file_path = "./data/adServiceHighCpu/original_metrics.json"
output_path = "./data/adServiceHighCpu/output/"
metric_file_name_one_row = 'original_metrics.json'
metric_file_name_multi_row = 'pretty_original_metrics.json'

# 기준 시간 설정 (예: 현재 시간)
log_start_time = "2024-08-21 22:25:38"

# 메트릭 파싱 함수 정의
def parse_metrics(file_path, metric_names, reference_time, minus_time_value):
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
                                    metric_time = convert_string_to_datetime(data_point.get("timeUnixNano"))
                                    if reference_time - timedelta(minutes=minus_time_value) <= metric_time <= reference_time:
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
                                    metric_time = convert_string_to_datetime(data_point.get("timeUnixNano"))
                                    if reference_time - timedelta(minutes=minus_time_value) <= metric_time <= reference_time:
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

metric_start_time = convert_string_to_datetime(log_start_time)

# 메트릭 파싱 및 출력
parsed_metrics = parse_metrics(file_path=json_file_path,
                               metric_names=metric_keys,
                               reference_time=metric_start_time,
                               minus_time_value=1)

# 메트릭 데이터를 파일에 저장 (한 줄)
with open(output_path + metric_file_name_one_row, 'w') as metric_output_file:
    json.dump(parsed_metrics, metric_output_file, separators=(',', ':'))

# 스팬 데이터를 파일에 저장 (여러 줄)
with open(output_path + metric_file_name_multi_row, 'w') as metric_output_file:
    json.dump(parsed_metrics, metric_output_file, indent=4)

# 결과 출력 (확인용)
print("파싱된 메트릭 데이터입니다:")
print(json.dumps(parsed_metrics, indent=4))