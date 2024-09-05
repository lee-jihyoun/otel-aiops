import json
import time
from datetime_util import change_timenano_format

# Trace_parser에서 할 일
# - filtered_span & original_span parsing
# - trace id 찾는 함수 : 500, error가 발생한 trace id를 찾기

# batch1
# 1. parsing_span()

# batch2
# 1. find_trace_id() -> return trace_ids {} / 500, error를 갖는 trace id 추출
# 2. extract_span_with_trace_id() / trace id에 맞는 span만 추출
# 3. parsing_span() / filtered_span, extraced_span 데이터 경우에 따라 make_parsed_info()를 호출하는 함수
# 4. make_parsed_info() / parsed_info를 만드는 함수. 디테일한 파싱 작업 수행

# 경로 설정
path = './data/paymentServiceFailure/'
output_path = path + 'output/'
file_name = 'filtered_span.json'
extraced_file_name = 'extracted_span_by_trace_id.json'


def make_parsed_info(span_data):
    for resource in span_data.get('resourceSpans', []):
        service_name = None
        os_type = None
        if "resource" in resource and "attributes" in resource["resource"]:
            for attribute in resource["resource"]["attributes"]:
                if attribute["key"] == "service.name":
                    service_name = attribute["value"]["stringValue"]
                if attribute["key"] == "os.type":
                    os_type = attribute["value"]["stringValue"]

        for scopeSpan in resource.get("scopeSpans", []):
            for span in scopeSpan.get("spans", []):
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
                for attribute in span.get("attributes", []):
                    try:
                        if attribute["key"] == "http.status_code":
                            parsed_info["http.status_code"] = attribute["value"]["intValue"]
                        elif attribute["key"] == "rpc.grpc.status_code":
                            parsed_info["rpc.grpc.status_code"] = attribute["value"]["intValue"]
                        elif attribute["key"] == "http.url":
                            parsed_info["http.url"] = attribute["value"]["stringValue"]
                        elif attribute["key"] == "rpc.method":
                            parsed_info["rpc.method"] = attribute["value"]["stringValue"]
                    except KeyError as e:
                        print(f"Key is not found: {e}")
                        continue

                for event in span.get("events", []):
                    for attribute in event.get("attributes", []):
                        if attribute["key"] == "exception.message":
                            parsed_info["exception.message"] = attribute["value"]["stringValue"]
                        elif attribute["key"] == "exception.stacktrace":
                            parsed_info["exception.stacktrace"] = attribute["value"]["stringValue"]

        return parsed_info


def parsing_span(path, file_name):
    filtered_spans = []
    with open(path + file_name, "r") as span_file:
        for line in span_file:
            try:
                span_data = json.loads(line.strip())
                change_timenano_format(span_data)

                # filtered_span 데이터를 파싱하는 경우(dict 타입)
                if isinstance(span_data, dict):
                    parsed_info = make_parsed_info(span_data)
                    filtered_spans.append(parsed_info)

                # extracted_span 데이터를 파싱하는 경우(list 타입)
                if isinstance(span_data, list):
                    for resourceSpan in span_data:
                        parsed_info = make_parsed_info(resourceSpan)
                        filtered_spans.append(parsed_info)

            except json.JSONDecodeError as e:
                print(f"Error parsing line: {e}")

    # 스팬 데이터를 파일에 저장 (한 줄)
    with open(output_path + file_name, 'w') as span_output_file:
        json.dump(filtered_spans, span_output_file, separators=(',', ':'))

    # 스팬 데이터를 pretty 파일에 저장 (여러 줄)
    with open(output_path + 'pretty_' + file_name, 'w') as span_output_file:
        json.dump(filtered_spans, span_output_file, indent=4)

    # 결과 출력 (확인용)
    print(json.dumps(filtered_spans, indent=4))


# 500, error 데이터를 갖는 trace id를 찾는 함수 (paymentService와 같은 경우)
def find_trace_id(path, file_name):
    trace_ids = {}
    idx = 0
    with (open(path + file_name, "r") as span_file):
        for line in span_file:
            idx += 1
            try:
                span_data = json.loads(line.strip())
                for resourceSpan in span_data.get('resourceSpans', []):
                    for scopeSpan in resourceSpan.get("scopeSpans", []):
                        for span in scopeSpan.get("spans", []):
                            trace_id = span.get("traceId")
                            for attribute in span.get("attributes", []):
                                try:
                                    if attribute["key"] == "http.status_code":
                                        value = attribute["value"].get("intValue")
                                        if value == "500":
                                            if trace_id:
                                                trace_ids[trace_id] = idx

                                except KeyError as e:
                                    print(f"Key is not found: {e}")
                                    continue

                            for event in span.get("events", []):
                                for attribute in event.get("attributes", []):
                                    if attribute["key"] == "exception.stacktrace":
                                        value = attribute["value"].get("stringValue")
                                        if "Error" in value:
                                            trace_ids[trace_id] = idx
            except json.JSONDecodeError as e:
                print(f"Error parsing line: {e}")

    print(trace_ids, f"total_traceId_cnt: {len(trace_ids)}")
    return trace_ids


# find_trace_id()로 나온 결과에 따라 해당되는 span을 추출하여 extraced json 파일을 새로 생성(단, list 형태임)
def extract_span_by_trace_id(trace_ids, path, file_name):
    extracted_spans = []
    with (open(path + file_name, "r") as span_file):
        for line in span_file:
            try:
                span_data = json.loads(line.strip())
                for resourceSpan in span_data.get('resourceSpans', []):
                    for scopeSpan in resourceSpan.get("scopeSpans", []):
                        for span in scopeSpan.get("spans", []):
                            trace_id = span.get("traceId")
                            if trace_id in trace_ids.keys():
                                extracted_spans.append(span_data)
            except json.JSONDecodeError as e:
                print(f"Error parsing line: {e}")

    # 스팬 데이터를 파일에 저장 (한 줄)
    with open(path + 'extracted_span_by_trace_id.json', 'w') as span_output_file:
        json.dump(extracted_spans, span_output_file, separators=(',', ':'))

    # 스팬 데이터를 pretty 파일에 저장 (여러 줄)
    with open(path + 'pretty_' + 'extracted_span_by_trace_id.json', 'w') as span_output_file:
        json.dump(extracted_spans, span_output_file, indent=4)


# 오류가 발생한 trace id만을 추출
extracted_trace_ids = find_trace_id(path, file_name)

# trace id와 일치하는 span만 추출
extract_span_by_trace_id(extracted_trace_ids, path, file_name)

# 파싱 후 1초 딜레이
time.sleep(1)

# case1. filtered_span 파싱하기(보통의 경우)
parsing_span(path, file_name)

# case2. extracted_span 파싱하기(paymentService와 같은 경우)
# parsing_span(path, extraced_file_name)
