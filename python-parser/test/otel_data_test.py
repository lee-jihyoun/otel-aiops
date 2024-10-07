import json
import time
from util.datetime_util import change_timenano_format
import os

# 경로 설정
# log_file_name = "filtered_logs.json"
# span_file_name = "filtered_span.json"

log_file_name = "original_logs.json"
span_file_name = "original_span.json"

folder_name = "241007_data_test"

log_file_path = "../../data" + "/" + folder_name + "/" + log_file_name
span_file_path = "../../data" + "/" + folder_name + "/" + span_file_name
output_path = "../../data" + "/" + folder_name + "/" + 'output/'

log_file_name_one_row = 'one_row_' + log_file_name
log_file_name_multi_row = 'multi_row_' + log_file_name

span_file_name_one_row = 'one_row_' + span_file_name
span_file_name_multi_row = 'multi_row_' + span_file_name

# 테스트용 데이터
test_log = "../../data" + "/" + folder_name + "/" + 'output/' + log_file_name_one_row
test_trace = "../../data" + "/" + folder_name + "/" + 'output/' + span_file_name_one_row


def parsing_log():
    # 경로에 폴더가 없으면 생성
    if not os.path.exists(output_path):
        os.makedirs(output_path)

    # 로그 데이터 파싱 및 필요한 key 값 추출
    filtered_logs = []

    with open(log_file_path, "r") as log_file:
        for line in log_file:
            try:
                log_data = json.loads(line.strip())
                change_timenano_format(log_data)  # 시간 전처리 적용

                for resource_log in log_data.get('resourceLogs', []):
                    parsed_log = {
                        "service.name": None,
                        "service.code": None,
                        "traceId": None,
                        "observedTimeUnixNano": None,  # 새로운 시간 필드 추가
                    }

                    # resource 부분에서 필요한 정보 추출
                    if "resource" in resource_log and "attributes" in resource_log["resource"]:
                        for attribute in resource_log["resource"]["attributes"]:
                            if attribute["key"] == "service.name":
                                parsed_log["service.name"] = attribute["value"]["stringValue"]
                            if attribute["key"] == "service.code":
                                parsed_log["service.code"] = attribute["value"]["stringValue"]

                    # scopeLogs와 logRecords에서 필요한 정보 추출
                    for scope_log in resource_log.get("scopeLogs", []):
                        for log_record in scope_log.get("logRecords", []):
                            if "observedTimeUnixNano" in log_record:
                                parsed_log["observedTimeUnixNano"] = log_record["observedTimeUnixNano"]
                            if "traceId" in log_record and log_record["traceId"] != "":
                                parsed_log["traceId"] = log_record["traceId"]
                                # traceId가 유효한 경우에만 logRecord 추가
                                filtered_logs.append(parsed_log)

            except json.JSONDecodeError as e:
                print(f"Error parsing line: {e}")

    # 로그 데이터를 파일에 저장 (한 줄)
    with open(output_path + log_file_name_one_row, 'w') as log_output_file:
        json.dump(filtered_logs, log_output_file, separators=(',', ':'))

    # 로그 데이터를 파일에 저장 (여러 줄)
    with open(output_path + log_file_name_multi_row, 'w') as log_output_file:
        json.dump(filtered_logs, log_output_file, indent=4)


def parsing_trace():
    # 스팬 데이터 파싱 및 필요한 key 값 추출
    filtered_spans = []

    with open(span_file_path, "r") as span_file:
        for line in span_file:
            try:
                span_data = json.loads(line.strip())
                change_timenano_format(span_data)  # 시간 전처리 적용

                for resource in span_data.get('resourceSpans', []):
                    service_name = None
                    service_code = None

                    # if "resource" in resource and "attributes" in resource["resource"]:
                    if "resource" in resource and "attributes" in resource["resource"]:
                        for attribute in resource["resource"]["attributes"]:
                            if attribute["key"] == "service.name":
                                service_name = attribute["value"]["stringValue"]
                            if attribute["key"] == "service.code":
                                service_code = attribute["value"]["stringValue"]

                    for scopeSpan in resource.get("scopeSpans", []):
                        for span in scopeSpan.get("spans", []):
                            # trace에서는 scopespan 안에 attribute가 따로 있음
                            for attribute in span.get("attributes", []):
                                parsed_info = {
                                    "service.name": service_name,
                                    "service.code": service_code,
                                    "traceId": span.get("traceId"),
                                    "spanId": span.get("spanId"),
                                    # "exception.stacktrace": None,
                                    "exception.stacktrace.short": None,
                                    "startTimeUnixNano": span.get("startTimeUnixNano"),
                                    "endTimeUnixNano": span.get("endTimeUnixNano")
                                }

                            # event 발생 시 event key 내에 exception.message와 exception.stacktrace가 따로 있음
                            for event in span.get("events", []):
                                for attribute in event.get("attributes", []):
                                    if attribute["key"] == "exception.stacktrace":
                                        # parsed_info["exception.stacktrace"] = attribute["value"]["stringValue"]
                                        # 두 번째 \n 전까지만 가져오기, 중간에 \n 존재 시 삭제
                                        parsed_info["exception.stacktrace.short"] = ' '.join(
                                            line.strip() for line in attribute["value"]["stringValue"].split('\n')[:2])

                                filtered_spans.append(parsed_info)

            except json.JSONDecodeError as e:
                print(f"Error parsing line: {e}")

    # 스팬 데이터를 파일에 저장 (한 줄)
    with open(output_path + span_file_name_one_row, 'w') as span_output_file:
        json.dump(filtered_spans, span_output_file, separators=(',', ':'))

    # 스팬 데이터를 파일에 저장 (여러 줄)
    with open(output_path + span_file_name_multi_row, 'w') as span_output_file:
        json.dump(filtered_spans, span_output_file, indent=4)


def make_test_data(test_log, test_trace):
    # 테스트 코드
    trace_id_list_log = []
    trace_id_list_trace = []
    with open(test_log, "r") as test_log:
        for line in test_log:
            full_data = json.loads(line.strip())
            for data in full_data:
                trace_id_list_log.append((data["traceId"], data["service.code"]))

    with open(test_trace, "r") as test_trace:
        for line in test_trace:
            full_data = json.loads(line.strip())
            for data in full_data:
                trace_id_list_trace.append((data["traceId"], data["service.code"]))

    return trace_id_list_log, trace_id_list_trace


def sample_test():
    tuple1 = [('test', 1), ('test2', 1)]
    tuple2 = [('test', 2), ('test2', 1)]
    intersection = list(set(tuple1) & set(tuple2))
    print(intersection)
    tuple_complement = list(set(tuple1).difference(tuple2))
    print(tuple_complement)


def data_test(trace_id_list_log, trace_id_list_trace):
    # # filtered 비교
    print("\n * log의 길이:", len(trace_id_list_log))
    print("\n * trace의 길이:", len(trace_id_list_trace))

    # 교집합
    intersection = list(set(trace_id_list_log) & set(trace_id_list_trace))
    print("\n * 교집합의 길이:", len(intersection))

    # 차집합
    log_complement = list(set(trace_id_list_log).difference(trace_id_list_trace))
    trace_complement = list(set(trace_id_list_trace).difference(trace_id_list_log))

    print("\n * log에는 있는데 trace에는 없는 id(차집합):", len(log_complement))
    print("\n * trace에는 있는데 loge에는 없는 id(차집합):", len(trace_complement))


parsing_log()
# 로그 파싱 후 1초 딜레이
time.sleep(1)
parsing_trace()
# 트레이스 파싱 후 1초 딜레이
time.sleep(1)
trace_id_list_log, trace_id_list_trace = make_test_data(test_log, test_trace)
data_test(trace_id_list_log, trace_id_list_trace)

'''
코드에서 서비스코드도 같이 비교


서버에서 테스트 방법
1. 기존에 쌓였던 데이터 삭제
    cd /opt/otel-aiops/spring-otel-listener
    rm -rf filtered_logs.json filtered_span.json filtered_logs.json_backup  filtered_span.json_backup  original_logs.json_backup original_metrics.json_backup original_span.json_backup nohub.out

2. otel listner 중지 
    ps -ef|grep spring 
    kill -9 
    
3. docker 중지
    docker stop $(docker ps -qa)
    
4. docker 이미지 삭제
    docker rm -f $(docker ps -qa)
    
5. spring-otel-listener 실행
    cd /opt/spring-otel-listener-run/
    nohup java -jar spring-otel-listener-0.0.1-SNAPSHOT.jar &

5. docker 캐시 삭제
    docker builder prune -f

6. docker 빌드
    docker compose up --build --force-recreate --remove-orphans --detach



2. otel demo 캐시 없이 빌드하기 
    - 조건. otel-listner 프로세스 끄고 나서
    - 오래 걸림. 최소 20분
3. otel demo 캐시 없이 빌드하기 
    - 조건. otelcol-config.yml 에 debug 로 바꾸고  
    - 경로: /opt/opentelemetry-demo/src/otelcollector
    
      filter/logs:
        logs:
          log_record:
            - 'severity_number < 10' # 10보다 작은건 거르겠다. 수집 안하겠다. INFO 레벨부터 수집
            
    (1~4,   5~8,   9~12, 14~16, 17~20, 21~24)
    (TRACE, DEBUG, INFO, WARN, ERROR, FATAL)

'''
