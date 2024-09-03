import json

# JSON 파일 경로 설정
json_file_path = "./data/adServiceHighCpu/original_metrics.json"
output_path = "./data/adServiceHighCpu/output/"
output_file_path = "./data/adServiceHighCpu/output/original_metrics.json"

# 여러 개의 JSON 객체를 라인별로 읽어오기
json_data = []
with open(json_file_path, "r") as json_file:
    for line in json_file:
        try:
            data = json.loads(line.strip())
            json_data.append(data)
        except json.JSONDecodeError as e:
            print(f"Error parsing line: {e}")


# process.runtime.cpython.memory와 process.runtime.cpython.cpu_time 메트릭을 파싱하는 함수
def parse_cpython_metrics(data):
    metrics_data = {"process.runtime.cpython.cpu_time": [], "process.runtime.cpython.memory": []}

    for resource_metric in data.get("resourceMetrics", []):
        for scope_metric in resource_metric.get("scopeMetrics", []):
            for metric in scope_metric.get("metrics", []):
                if metric.get("name") in metrics_data:
                    for data_point in metric.get("sum", {}).get("dataPoints", []):
                        metric_info = {
                            "type": None,
                            "startTimeUnixNano": data_point.get("startTimeUnixNano"),
                            "timeUnixNano": data_point.get("timeUnixNano"),
                            "value": data_point.get("asDouble", data_point.get("asInt"))
                        }
                        for attribute in data_point.get("attributes", []):
                            if attribute.get("key") == "type":
                                metric_info["type"] = attribute.get("value", {}).get("stringValue")
                        metrics_data[metric.get("name")].append(metric_info)

    return metrics_data

# 각 JSON 객체에서 process.runtime.cpython.memory와 process.runtime.cpython.cpu_time 데이터를 파싱
for data in json_data:
    metrics_data = parse_cpython_metrics(data)
    if metrics_data:
        for key, metric_entries in metrics_data.items():
            if metric_entries:
                print(f"\n{key}:")
                for entry in metric_entries:
                    print(f"Type: {entry['type']}, Start Time: {entry['startTimeUnixNano']}, End Time: {entry['timeUnixNano']}, Value: {entry['value']}")
    else:
        print("No relevant data found.")

metrics_data = []
# 메트릭 파싱 함수 정의
def parse_metrics(data_list, metric_name, value_key="asDouble"):
    for data in data_list:
        for resource_metric in data.get("resourceMetrics", []):
            for scope_metric in resource_metric.get("scopeMetrics", []):
                for metric in scope_metric.get("metrics", []):
                    if metric.get("name") == metric_name:
                        for data_point in metric.get("sum", {}).get("dataPoints", []):
                            metric_info = {
                                "metric_name": metric_name,  # 메트릭 이름 추가
                                "type": None,
                                "startTimeUnixNano": data_point.get("startTimeUnixNano"),
                                "timeUnixNano": data_point.get("timeUnixNano"),
                                "value": data_point.get(value_key)
                            }
                            for attribute in data_point.get("attributes", []):
                                if attribute.get("key") == "type":
                                    metric_info["type"] = attribute.get("value", {}).get("stringValue")
                            metrics_data.append(metric_info)
                        for data_point in metric.get("gauge", {}).get("dataPoints", []):
                            metric_info = {
                                "metric_name": metric_name,  # 메트릭 이름 추가
                                "type": None,
                                "startTimeUnixNano": data_point.get("startTimeUnixNano"),
                                "timeUnixNano": data_point.get("timeUnixNano"),
                                "value": data_point.get(value_key)
                            }
                            for attribute in data_point.get("attributes", []):
                                if attribute.get("key") == "type":
                                    metric_info["type"] = attribute.get("value", {}).get("stringValue")
                            metrics_data.append(metric_info)
    return metrics_data

# 각 메트릭 파싱 및 출력
cpu_time_data = parse_metrics(json_data, "process.runtime.cpython.cpu_time", value_key="asDouble")
memory_data = parse_metrics(json_data, "process.runtime.cpython.memory", value_key="asInt")
cpu_utilization_data = parse_metrics(json_data, "process.runtime.cpython.cpu.utilization", value_key="asDouble")

# 스팬 데이터를 파일에 저장 (한 줄)
with open(output_path + 'original_metrics.json', 'w') as span_output_file:
    json.dump(metrics_data, span_output_file, separators=(',', ':'))

print(cpu_time_data)

# 결과 출력
print("CPU Time Data:")