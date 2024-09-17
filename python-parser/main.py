import threading
from batch import parser_batch
import psycopg2  # pip install psycopg2-binary
import re
import requests
import json
import variables.trace_id as trace_id

print("==============")
# # trace_id_dict 테스트용
# trace_id.trace_id_dict["main"] = ""
# print("main: ", trace_id.trace_id_dict)

thread1 = threading.Thread(target=parser_batch.run_batch1)  # 각 batch를 실행할 스레드를 생성
thread1.start()  # 스레드를 시작 (동시에 실행)
thread1.join()  # 스레드가 종료될 때까지 대기


# response에 마크다운이 포함된 경우 escape 문자열 처리
def make_clean_markdown_json(markdown_json):
    # 1. ```json, ```plaintext, ```bash 등의 불필요한 코드 블록 제거
    cleaned_str = re.sub(r"```(json|plaintext|bash)?\n?", "", markdown_json)

    # 2. 공백과 줄바꿈 제거
    # \n -> 공백으로 변환
    cleaned_str = re.sub(r'\\n', '', cleaned_str)
    # 연속적인 공백을 하나의 공백으로 축소
    cleaned_str = re.sub(r'\s+', ' ', cleaned_str).strip()

    # 3. 이스케이프 문자 제거
    # \" -> " 로 변환
    cleaned_str = cleaned_str.replace('\\"', '"')
    # \ -> /로 변환
    cleaned_str = cleaned_str.replace('\\', '/')

    # 4. 특수 문자열 패턴 처리
    # '"{' -> '{' 로 변경
    cleaned_str = re.sub(r'"\{', '{', cleaned_str)
    # '}"' -> '}' 로 변경
    cleaned_str = re.sub(r'\}"', '}', cleaned_str)
    # \\/ -> / 로 변경
    cleaned_str = cleaned_str.replace('\\/', '/')
    # // 제거
    cleaned_str = cleaned_str.replace('//', '')

    # 5. JSON 변환 시 문제가 될 수 있는 불필요한 공백 제거
    # "key": "value"와 같은 패턴에서 key와 value 사이의 공백 정리
    cleaned_str = re.sub(r'"\s*:\s*"', '":"', cleaned_str)

    # 잘못된 JSON 문자열 디버깅
    try:
        freesia_result = json.loads(cleaned_str)
    except json.JSONDecodeError as e:
        print("* JSON 디코딩 에러:", e)
        print("* 문제 있는 문자열 주변:", cleaned_str[max(0, e.pos-60):e.pos+60])
        print("============== api result DB insert 실패 ==============")
    return freesia_result


def remove_json_value(value):
    # print('* in remove_json_value 함수:', value)
    value = value.replace("{", "(").replace("}", ")")
    return value


# reponse["data"]["content"]가 깔끔한 json으로 오는 경우
def make_db_data(clean_response):
    content = clean_response["data"]["content"]
    error_report = {}
    for k, v in content.items():
        service_name = content["기본정보"]["서비스명(영문)"]
        error_name = content["오류내용"]["오류 이름"]
        error_create_time = content["오류내용"]["발생 시간"]
        error_content = content["오류내용"]["오류 내용"]
        error_location = content["분석결과"]["오류 발생 위치"]
        error_cause = content["분석결과"]["오류 근본 원인"]
        service_impact = content["분석결과"]["서비스 영향도"]
        error_solution = content["후속조치"]["조치방안"]

        error_report["error_name"] = error_name
        error_report["error_create_time"] = error_create_time
        error_report["error_content"] = error_content
        error_report["error_location"] = error_location
        error_report["error_cause"] = error_cause
        error_report["service_impact"] = service_impact
        error_report["error_solution"] = error_solution
        return service_name, error_report


def db_connection():
    connection = psycopg2.connect(
        host='100.83.227.59',
        port=5532,
        user='test_admin',
        password='new1234!',
        database='rnp'
    )
    cursor = connection.cursor()
    return connection, cursor


def select_data(connection, cursor):
    read_query = """
            SELECT error_content
            FROM error_report
    """
    cursor.execute(read_query)
    result = cursor.fetchall()
    print(result)

def find_service_code(cursor, service_name):
    select_query = f"""
            SELECT service_code
            FROM service_info
            where service_name_eng = '{service_name}'
    """
    cursor.execute(select_query)
    result = cursor.fetchone()
    return result[0]

def insert_data(connection, cursor, dbdata, service_code):
    data_to_insert = {
        "service_code": service_code,
        "error_name": dbdata['error_name'],
        "error_content": dbdata['error_content'],
        "error_location": dbdata['error_location'],
        "error_cause": dbdata['error_cause'],
        "error_create_time": dbdata['error_create_time'],
        "service_impact": dbdata['service_impact'],
        "error_solution": dbdata['error_solution']
    }
    # SQL 쿼리 생성 및 실행
    insert_query = """
            INSERT INTO error_report (
                service_code,
                error_name, 
                error_content, 
                error_location, 
                error_cause, 
                error_create_time, 
                service_impact,
                error_solution
            ) VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
        """
    try:
        cursor.execute(insert_query, (
            data_to_insert["service_code"],
            data_to_insert["error_name"],
            data_to_insert["error_content"],
            data_to_insert["error_location"],
            data_to_insert["error_cause"],
            data_to_insert["error_create_time"],
            data_to_insert["service_impact"],
            data_to_insert["error_solution"]
        ))

        # 변경사항 저장
        connection.commit()
    finally:
        connection.close()


# DB에서 API key 읽어오기
def select_api_key(connection, cursor):
    read_query = """
            SELECT api_service_token
            FROM api_auth_tokens
            where api_service_name = 'freesia_api'
    """
    cursor.execute(read_query)
    result = cursor.fetchone()
    return result[0]


conn, cur = db_connection()


# freesia api 연동
url = "http://freesia.run:8080/openapi/v1/chat"
api_key = select_api_key(conn, cur)


# 프리지아 호출
def call_freesia_api(json_data):
    headers = {
        "X-API-KEY": api_key,
        "content-type": "application/json"
    }
    response = requests.post(url, data=json_data, headers=headers)
    return response


# 보낼 json 데이터의 message 생성
def create_message(log_data, span_data):
    f = open("prompt_template.txt", 'r', encoding='UTF8')
    data = f.read()
    data = data.replace("{{error_log}}", log_data)
    data = data.replace("{{error_span}}", span_data)
    data = {"message": data}
    json_data = json.dumps(data)
    return json_data


# 오류 리포트 생성
def create_error_report(log_data, span_data):
    json_data = create_message(log_data, span_data)
    result = call_freesia_api(json_data)
    return result.text

# api 호출용 데이터
log_data = """
{
        "container.id": null,
        "os.description": null,
        "process.command_line": null,
        "service.name": "currencyservice",
        "telemetry.sdk.language": "cpp",
        "logRecords_severityText": "INFO",
        "logRecords_body_stringValue": "Convert conversion successful",
        "traceId": "7097e6b36b89fb6be8fcbbaafffe1302",
        "observedTimeUnixNano": "2024-08-21 23:00:26"
    },
    {
        "container.id": null,
        "os.description": null,
        "process.command_line": null,
        "service.name": "currencyservice",
        "telemetry.sdk.language": "cpp",
        "logRecords_severityText": "INFO",
        "logRecords_body_stringValue": "Convert conversion successful",
        "traceId": "7097e6b36b89fb6be8fcbbaafffe1302",
        "observedTimeUnixNano": "2024-08-21 23:00:26"
    },
    {
        "container.id": null,
        "os.description": null,
        "process.command_line": null,
        "service.name": "currencyservice",
        "telemetry.sdk.language": "cpp",
        "logRecords_severityText": "INFO",
        "logRecords_body_stringValue": "Convert conversion successful",
        "traceId": "7097e6b36b89fb6be8fcbbaafffe1302",
        "observedTimeUnixNano": "2024-08-21 23:00:26"
    }
"""
span_data = """
{
        "service.name": "checkoutservice",
        "os.type": "linux",
        "traceId": "7097e6b36b89fb6be8fcbbaafffe1302",
        "spanId": "63227652df31b934",
        "name": "oteldemo.PaymentService/Charge",
        "http.status_code": null,
        "rpc.grpc.status_code": "2",
        "exception.message": null,
        "exception.stacktrace": null,
        "http.url": null,
        "rpc.method": "Charge",
        "startTimeUnixNano": "2024-08-21 23:00:26",
        "endTimeUnixNano": "2024-08-21 23:00:26"
    },
    {
        "service.name": "checkoutservice",
        "os.type": "linux",
        "traceId": "7097e6b36b89fb6be8fcbbaafffe1302",
        "spanId": "11549d72d2032a27",
        "name": "oteldemo.CheckoutService/PlaceOrder",
        "http.status_code": null,
        "rpc.grpc.status_code": "13",
        "exception.message": "could not charge the card: rpc error: code = Unknown desc = PaymentService Fail Feature Flag Enabled",
        "exception.stacktrace": null,
        "http.url": null,
        "rpc.method": "PlaceOrder",
        "startTimeUnixNano": "2024-08-21 23:00:26",
        "endTimeUnixNano": "2024-08-21 23:00:26"
    },
    {
        "service.name": "frontend",
        "os.type": "linux",
        "traceId": "7097e6b36b89fb6be8fcbbaafffe1302",
        "spanId": "98c7119541a153fb",
        "name": "executing api route (pages) /api/checkout",
        "http.status_code": "500",
        "rpc.grpc.status_code": null,
        "exception.message": "13 INTERNAL: failed to charge card: could not charge the card: rpc error: code = Unknown desc = PaymentService Fail Feature Flag Enabled",
        "exception.stacktrace": "Error: 13 INTERNAL: failed to charge card: could not charge the card: rpc error: code = Unknown desc = PaymentService Fail Feature Flag Enabled\n    at callErrorFromStatus (/app/node_modules/@grpc/grpc-js/build/src/call.js:31:19)\n    at Object.onReceiveStatus (/app/node_modules/@grpc/grpc-js/build/src/client.js:193:76)\n    at Object.onReceiveStatus (/app/node_modules/@grpc/grpc-js/build/src/client-interceptors.js:360:141)\n    at Object.onReceiveStatus (/app/node_modules/@grpc/grpc-js/build/src/client-interceptors.js:323:181)\n    at /app/node_modules/@grpc/grpc-js/build/src/resolving-call.js:129:78\n    at process.processTicksAndRejections (node:internal/process/task_queues:77:11)\nfor call at\n    at ServiceClientImpl.makeUnaryRequest (/app/node_modules/@grpc/grpc-js/build/src/client.js:161:32)\n    at ServiceClientImpl.<anonymous> (/app/node_modules/@grpc/grpc-js/build/src/make-client.js:105:19)\n    at /app/node_modules/@opentelemetry/instrumentation-grpc/build/src/clientUtils.js:131:31\n    at /app/node_modules/@opentelemetry/instrumentation-grpc/build/src/instrumentation.js:211:209\n    at AsyncLocalStorage.run (node:async_hooks:346:14)\n    at AsyncLocalStorageContextManager.with (/app/node_modules/@opentelemetry/context-async-hooks/build/src/AsyncLocalStorageContextManager.js:33:40)\n    at ContextAPI.with (/app/node_modules/@opentelemetry/api/build/src/api/context.js:60:46)\n    at ServiceClientImpl.clientMethodTrace [as placeOrder] (/app/node_modules/@opentelemetry/instrumentation-grpc/build/src/instrumentation.js:211:42)\n    at /app/.next/server/pages/api/checkout.js:1:1041\n    at new ZoneAwarePromise (/app/node_modules/zone.js/bundles/zone.umd.js:1340:33)",
        "http.url": null,
        "rpc.method": null,
        "startTimeUnixNano": "2024-08-21 23:00:26",
        "endTimeUnixNano": "2024-08-21 23:00:26"
    },
    {
        "service.name": "frontend",
        "os.type": "linux",
        "traceId": "7097e6b36b89fb6be8fcbbaafffe1302",
        "spanId": "be50c0fcc088f2ea",
        "name": "POST",
        "http.status_code": "500",
        "rpc.grpc.status_code": null,
        "exception.message": null,
        "exception.stacktrace": null,
        "http.url": "http://frontend-proxy:8080/api/checkout",
        "rpc.method": null,
        "startTimeUnixNano": "2024-08-21 23:00:26",
        "endTimeUnixNano": "2024-08-21 23:00:26"
    },
    {
        "service.name": "frontend",
        "os.type": "linux",
        "traceId": "7097e6b36b89fb6be8fcbbaafffe1302",
        "spanId": "5e3d8f0e54ca4696",
        "name": "grpc.oteldemo.CheckoutService/PlaceOrder",
        "http.status_code": null,
        "rpc.grpc.status_code": "13",
        "exception.message": null,
        "exception.stacktrace": null,
        "http.url": null,
        "rpc.method": "PlaceOrder",
        "startTimeUnixNano": "2024-08-21 23:00:26",
        "endTimeUnixNano": "2024-08-21 23:00:26"
    },
    {
        "service.name": "loadgenerator",
        "os.type": null,
        "traceId": "7097e6b36b89fb6be8fcbbaafffe1302",
        "spanId": "ed013ccaa25fdb34",
        "name": "POST",
        "http.status_code": "500",
        "rpc.grpc.status_code": null,
        "exception.message": null,
        "exception.stacktrace": null,
        "http.url": "http://frontend-proxy:8080/api/checkout",
        "rpc.method": null,
        "startTimeUnixNano": "2024-08-21 23:00:26",
        "endTimeUnixNano": "2024-08-21 23:00:26"
    },
    {
        "service.name": "paymentservice",
        "os.type": "linux",
        "traceId": "7097e6b36b89fb6be8fcbbaafffe1302",
        "spanId": "e88b55d75ac1a487",
        "name": "grpc.oteldemo.PaymentService/Charge",
        "http.status_code": null,
        "rpc.grpc.status_code": null,
        "exception.message": "PaymentService Fail Feature Flag Enabled",
        "exception.stacktrace": "Error: PaymentService Fail Feature Flag Enabled\n    at module.exports.charge (/usr/src/app/charge.js:21:11)\n    at process.processTicksAndRejections (node:internal/process/task_queues:95:5)\n    at async Object.chargeServiceHandler [as charge] (/usr/src/app/index.js:21:22)",
        "http.url": null,
        "rpc.method": "Charge",
        "startTimeUnixNano": "2024-08-21 23:00:26",
        "endTimeUnixNano": "2024-08-21 23:00:26"
    }
"""

# # API 호출 및 DB insert 연동 테스트
# # 오류 내용(exception.stacktrace)에 {}가 포함된 경우 전처리하여 api 호출(ex: adServiceFailure)
# log_data = remove_json_value(log_data)
# # freesia api 호출
# response = create_error_report(log_data, span_data)
# print('\n * response data:', response)
# # response 데이터 escape 문자열 처리
# clean_result = make_clean_markdown_json(response)
# print('\n * clean_result:', clean_result)
# # DB insert를 위해 response 데이터 파싱
# service_name, db_data = make_db_data(clean_result)
# print('\n * db_data:', db_data)
# # response의 service_name을 이용하여 DB에서 sevice_code를 조회함
# service_code = find_service_code(cur, service_name)
# insert_data(conn, cur, db_data, service_code)
# print("============== api result DB insert 완료 ==============")

