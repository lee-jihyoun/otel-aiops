import threading
from batch import parser_batch
import psycopg2 # pip install psycopg2-binary
import re
import requests
import json

import variables.trace_id as trace_id

print("==============")
# # trace_id_dict 테스트용
# trace_id.trace_id_dict["main"] = ""
# print("main: ", trace_id.trace_id_dict)

thread1 = threading.Thread(target=parser_batch.run_batch1) # 각 batch를 실행할 스레드를 생성
thread1.start() # 스레드를 시작 (동시에 실행)
thread1.join() # 스레드가 종료될 때까지 대기


## freesia API return 결과를 DB에 저장
# 1. value로 null이 들어올 경우, ""로 replace
# 2. json의 data.content의 value를 DB 칼럼에 맞게 parsing
# 3. DB insert
# transaction 설정해주기.

# 비교를 위해 DB에 저장된 exception stacktrace 조회해오기

api_result = {
    "code": "0000",
    "message": "Success",
    "data": {
        "runId": "run-c4a33c3f-671f-49c1-9a77-7174caf25ea4-0",
        "content": "## 기본정보\n- **서비스명(영문)**: checkoutservice\n- **서비스명(한글)**: 체크아웃 서비스\n- **서비스코드**: CH1004\n- **서비스개요**: Go 언어로 개발된 서비스로, 사용자의 장바구니를 가져와 주문을 준비하고, 결제, 배송, 이메일 알림을 조정하는 서비스입니다.\n\n## 오류내용\n- **오류 이름**: oteldemo.CheckoutService/PlaceOrder\n- **발생 시간**: 2024-08-21 23:00:26\n- **오류 내용**: could not charge the card: rpc error: code = Unknown desc = PaymentService Fail Feature Flag Enabled\n\n## 분석결과\n- **오류 발생 위치**: 오류는 체크아웃 서비스(CheckoutService)의 PlaceOrder 메서드에서 발생하였으며, 이후 결제 서비스(PaymentService)의 charge 메서드로 전파되었습니다. stacktrace에서 아래와 같은 에러가 발생하였습니다:\n```plaintext\nError: PaymentService Fail Feature Flag Enabled\n    at module.exports.charge (/usr/src/app/charge.js:21:11)\n    at process.processTicksAndRejections (node:internal/process/task_queues:95:5)\n    at async Object.chargeServiceHandler [as charge] (/usr/src/app/index.js:21:22)\n```\n- **오류 근본 원인**:\n  1. 결제 서비스(PaymentService)에서 \"PaymentService Fail Feature Flag Enabled\" 에러가 발생하였습니다.\n  2. 이는 결제 기능이 비활성화된 상태에서 결제를 시도하여 발생한 문제입니다.\n  3. traceId \"7097e6b36b89fb6be8fcbbaafffe1302\"와 spanId \"e88b55d75ac1a487\"를 통해 오류가 결제 서비스로부터 시작되었음을 확인할 수 있습니다.\n\n## 후속조치\n- **조치방안**:\n  1. **PaymentService 설정 확인**:\n     - 결제 서비스의 설정 파일을 열어 \"Fail Feature Flag\"가 활성화되어 있는지 확인합니다.\n     - 설정 파일은 `/usr/src/app/config/settings.json` 또는 유사한 경로에 위치할 수 있습니다.\n     - 아래 명령어를 사용하여 설정 파일을 열어봅니다:\n     ```bash\n     nano /usr/src/app/config/settings.json\n     ```\n     - 설정 파일에서 \"Fail Feature Flag\"를 비활성화합니다.\n     예:\n     ```json\n     {\n       \"FailFeatureFlag\": false\n     }\n     ```\n  2. **서비스 재시작**:\n     - 설정 파일을 수정한 후, 결제 서비스를 재시작합니다. 아래 명령어를 사용하여 Docker 컨테이너를 재시작할 수 있습니다:\n     ```bash\n     docker restart paymentservice\n     ```\n  3. **로그 및 모니터링**:\n     - 변경 후, Opentelemetry를 통해 로그와 메트릭을 모니터링하여 동일한 오류가 다시 발생하는지 확인합니다.\n     - 특히, 결제 요청과 관련된 로그를 집중적으로 모니터링합니다.\n  4. **테스트 수행**:\n     - 설정 변경 후 결제 기능이 정상적으로 작동하는지 테스트합니다.\n     - 다양한 시나리오를 통해 결제 프로세스가 정상적으로 완료되는지 확인합니다.",
        "chatMemoryId": "97bf0bb6-1f94-42b3-9b06-3d82d4875c80",
        "promptTokens": 5908,
        "completionTokens": 742,
        "totalTokens": 6650,
        "turnId": "5b73dead-1f6c-4c61-aff2-690aac59ae29",
        "reference": [
            {
                "fileName": "service_rag_total_수정.txt",
                "page": "",
                "score": 0.6255208440280215,
                "content": "<서비스 아키텍처>\ngraph TD\nsubgraph Service Diagram\naccountingservice(Accounting Service):::dotnet\nadservice(Ad Service):::java\ncache[(Cache<br/>&#40redis&#41)]\ncartservice(Cart Service):::dotnet\ncheckoutservice(Checkout Service):::golang\ncurrencyservice(Currency Service):::cpp\nemailservice(Email Service):::ruby\nfrauddetectionservice(Fraud Detection Service):::kotlin\nfrontend(Frontend):::typescript\nfrontendproxy(Frontend Proxy <br/>&#40Envoy&#41):::cpp\nimageprovider(Image Provider <br/>&#40nginx&#41):::cpp\nloadgenerator([Load Generator]):::python\npaymentservice(Payment Service):::javascript\nproductcatalogservice(Product Catalog Service):::golang\nquoteservice(Quote Service):::php\nrecommendationservice(Recommendation Service):::python\nshippingservice(Shipping Service):::rust\nqueue[(queue<br/>&#40Kafka&#41)]\n\nInternet -->|HTTP| frontendproxy\nfrontendproxy -->|HTTP| frontend\nloadgenerator -->|HTTP| frontendproxy\nfrontendproxy -->|HTTP| imageprovider"
            },
            {
                "fileName": "service_rag_total_수정.txt",
                "page": "",
                "score": 0.539260745048523,
                "content": "<서비스 설명>\naccountingservice: .NET 언어로 개발된 서비스로, 들어오는 주문을 처리하고 모든 주문의 합계를 계산하는 서비스입니다. \nadservice: Java 언어로 개발된 서비스로, 주어진 문맥 단어에 기반하여 텍스트 광고를 제공하는 서비스입니다. \ncartservice: .NET 언어로 개발된 서비스로, 사용자의 장바구니에 있는 항목을 Redis에 저장하고 이를 다시 가져오는 서비스입니다. \ncheckoutservice: Go 언어로 개발된 서비스로, 사용자의 장바구니를 가져와 주문을 준비하고, 결제, 배송, 이메일 알림을 조정하는 서비스입니다.\ncurrencyservice: C++ 언어로 개발된 서비스로, 통화 금액을 다른 통화로 변환하는 서비스입니다. \nemailservice: Ruby 언어로 개발된 서비스로, 사용자에게 주문 확인 이메일을 보내는 서비스입니다. \nfrauddetectionservice: Kotlin 언어로 개발된 서비스로, 들어오는 주문을 분석하고 사기 시도를 탐지하는 서비스입니다. \nfrontend: JavaScript 언어로 개발된 프론트엔드 서비스로, 웹사이트를 제공하기 위해 HTTP 서버를 노출하며, 회원 가입이나 로그인이 필요하지 않으며, 모든 사용자에게 세션 ID를 자동으로 생성하는 서비스입니다. \nloadgenerator: Python/Locust 언어로 개발된 부하 생성기로, 실제 사용자 쇼핑 흐름을 모방하여 프론트엔드에 지속적으로 요청을 보내는 서비스입니다. \npaymentservice: JavaScript 언어로 개발된 서비스로, 제품 결제를 위해 주어진 신용 카드 정보로 해당 금액을 청구하고 거래 ID를 반환하는 서비스입니다. \nproductcatalogservice: Go 언어로 개발된 서비스로, 제품 목록을 제공하며, 제품을 검색하고 개별 제품을 얻을 수 있는 서비스입니다."
            }
        ]
    }
}


def make_db_data():
    data = {}
    try:
        for k, v in api_result.items():
            content = api_result["data"]["content"]

            # 정규 표현식 패턴을 이용해 값 추출
            service_code_match = re.search(r"서비스코드\*\*:\s*(\w+).*", content)
            error_name_match = re.search(r"오류 이름\*\*:\s*([^\n]+)", content)
            error_content_match = re.search(r"오류 내용\*\*:\s*([^\n]+)", content)
            error_location_match = re.search(r"오류 발생 위치\*\*:\s*([^\n]+)", content)
            error_cause_match = re.search(r"오류 근본 원인\*\*:\s*([^\n]+)", content)
            error_created_time_match = re.search(r"발생 시간\*\*:\s*([^\n]+)", content)
            # error_solution_match = re.search(r"조치방안\*\*:\s*([^\n]+)", content)

            service_code = service_code_match.group(1) if service_code_match else None
            error_name = error_name_match.group(1) if error_name_match else None
            error_content = error_content_match.group(1) if error_content_match else None
            error_location = error_location_match.group(1) if error_location_match else None
            error_cause = error_cause_match.group(1) if error_cause_match else None
            error_created_time = error_created_time_match.group(1) if error_created_time_match else None
            # error_solution = error_solution_match.group(1) if error_solution_match else None

            data["service_code"] = service_code
            data["error_name"] = error_name
            data["error_content"] = error_content
            data["error_location"] = error_location
            data["error_cause"] = error_cause
            data["error_created_time"] = error_created_time
            # data["error_solution"] = error_solution
            return data

    except NameError as e:
        print(f"Error parsing line: {e}")


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


# def insert_data(connection, cursor, self, db_data):
def insert_data(connection, cursor, dbdata):
    data_to_insert = {
        "service_code": dbdata['service_code'],
        "error_name": dbdata['error_name'],
        "error_content": dbdata['error_content'],
        "error_location": dbdata['error_location'],
        "error_cause": dbdata['error_cause'],
        "error_created_time": dbdata['error_created_time']
        # "error_solution": dbdata['error_solution']
    }
    # SQL 쿼리 생성 및 실행
    insert_query = """
            INSERT INTO error_report (
                service_code, error_name, error_content, error_location, error_cause, error_created_time
            ) VALUES (%s, %s, %s, %s, %s, %s)
        """
    try:
        cursor.execute(insert_query, (
            data_to_insert["service_code"],
            data_to_insert["error_name"],
            data_to_insert["error_content"],
            data_to_insert["error_location"],
            data_to_insert["error_cause"],
            data_to_insert["error_created_time"]
            # data_to_insert["error_solution"]
        ))

        # 변경사항 저장
        connection.commit()
    finally:
        connection.close()


conn, cur = db_connection()
# db_data = make_db_data()
# print(db_data)
# insert_data(conn, cur, db_data)
# select_data(conn, cur)

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

api_key = select_api_key(conn, cur)


## freesia api 연동
url = "http://freesia.run:8080/openapi/v1/chat"
data = {
    "message": "안녕. 착상에 대해 알려줘.",
    "chatMemoryId": "ffd46fac-5e8d-43d6-803a-d060766e259c"
}
# prompt_data = {"message": "{\"resourceSpans\":[{\"resource\":{\"attributes\":[{\"key\":\"service.name\",\"value\":{\"stringValue\":\"frontend\"}},{\"key\":\"telemetry.sdk.language\",\"value\":{\"stringValue\":\"nodejs\"}},{\"key\":\"telemetry.sdk.name\",\"value\":{\"stringValue\":\"opentelemetry\"}},{\"key\":\"telemetry.sdk.version\",\"value\":{\"stringValue\":\"1.25.1\"}},{\"key\":\"container.id\",\"value\":{\"stringValue\":\"f27bf1b161b28b909d52572607c84c667f42895393b06247598ceea61021aef4\"}},{\"key\":\"docker.cli.cobra.command_path\",\"value\":{\"stringValue\":\"docker compose\"}},{\"key\":\"host.name\",\"value\":{\"stringValue\":\"f27bf1b161b2\"}},{\"key\":\"host.arch\",\"value\":{\"stringValue\":\"amd64\"}},{\"key\":\"os.type\",\"value\":{\"stringValue\":\"linux\"}},{\"key\":\"os.version\",\"value\":{\"stringValue\":\"5.15.153.1-microsoft-standard-WSL2\"}},{\"key\":\"process.pid\",\"value\":{\"intValue\":\"17\"}},{\"key\":\"process.executable.name\",\"value\":{\"stringValue\":\"node\"}},{\"key\":\"process.executable.path\",\"value\":{\"stringValue\":\"/usr/local/bin/node\"}},{\"key\":\"process.command_args\",\"value\":{\"arrayValue\":{\"values\":[{\"stringValue\":\"/usr/local/bin/node\"},{\"stringValue\":\"--require\"},{\"stringValue\":\"./Instrumentation.js\"},{\"stringValue\":\"/app/server.js\"}]}}},{\"key\":\"process.runtime.version\",\"value\":{\"stringValue\":\"20.16.0\"}},{\"key\":\"process.runtime.name\",\"value\":{\"stringValue\":\"nodejs\"}},{\"key\":\"process.runtime.description\",\"value\":{\"stringValue\":\"Node.js\"}},{\"key\":\"process.command\",\"value\":{\"stringValue\":\"/app/server.js\"}},{\"key\":\"process.owner\",\"value\":{\"stringValue\":\"nextjs\"}}]},\"scopeSpans\":[{\"scope\":{\"name\":\"@opentelemetry/instrumentation-grpc\",\"version\":\"0.52.1\"},\"spans\":[{\"traceId\":\"a3068c5690d7e955872ea04eb2f2859b\",\"spanId\":\"428b07968ae20727\",\"parentSpanId\":\"d242dc005baabd8f\",\"name\":\"grpc.oteldemo.AdService/GetAds\",\"kind\":3,\"startTimeUnixNano\":\"1724248066953000000\",\"endTimeUnixNano\":\"1724248066960431536\",\"attributes\":[{\"key\":\"rpc.system\",\"value\":{\"stringValue\":\"grpc\"}},{\"key\":\"rpc.method\",\"value\":{\"stringValue\":\"GetAds\"}},{\"key\":\"rpc.service\",\"value\":{\"stringValue\":\"oteldemo.AdService\"}},{\"key\":\"net.peer.name\",\"value\":{\"stringValue\":\"adservice\"}},{\"key\":\"net.peer.port\",\"value\":{\"intValue\":\"9555\"}},{\"key\":\"rpc.grpc.status_code\",\"value\":{\"intValue\":\"14\"}},{\"key\":\"grpc.error_name\",\"value\":{\"stringValue\":\"Error\"}},{\"key\":\"grpc.error_message\",\"value\":{\"stringValue\":\"14 UNAVAILABLE: \"}}],\"status\":{\"code\":2}}]},{\"scope\":{\"name\":\"next.js\",\"version\":\"0.0.1\"},\"spans\":[{\"traceId\":\"a3068c5690d7e955872ea04eb2f2859b\",\"spanId\":\"d242dc005baabd8f\",\"parentSpanId\":\"9c1af4a84e49fa76\",\"name\":\"executing api route (pages) /api/data\",\"kind\":1,\"startTimeUnixNano\":\"1724248066953000000\",\"endTimeUnixNano\":\"1724248066960992817\",\"attributes\":[{\"key\":\"next.span_name\",\"value\":{\"stringValue\":\"executing api route (pages) /api/data\"}},{\"key\":\"next.span_type\",\"value\":{\"stringValue\":\"Node.runHandler\"}},{\"key\":\"http.status_code\",\"value\":{\"intValue\":\"500\"}}],\"events\":[{\"timeUnixNano\":\"1724248066960608243\",\"name\":\"exception\",\"attributes\":[{\"key\":\"exception.type\",\"value\":{\"stringValue\":\"14\"}},{\"key\":\"exception.message\",\"value\":{\"stringValue\":\"14 UNAVAILABLE: \"}},{\"key\":\"exception.stacktrace\",\"value\":{\"stringValue\":\"Error: 14 UNAVAILABLE: \\n    at callErrorFromStatus (/app/node_modules/@grpc/grpc-js/build/src/call.js:31:19)\\n    at Object.onReceiveStatus (/app/node_modules/@grpc/grpc-js/build/src/client.js:193:76)\\n    at Object.onReceiveStatus (/app/node_modules/@grpc/grpc-js/build/src/client-interceptors.js:360:141)\\n    at Object.onReceiveStatus (/app/node_modules/@grpc/grpc-js/build/src/client-interceptors.js:323:181)\\n    at /app/node_modules/@grpc/grpc-js/build/src/resolving-call.js:129:78\\n    at process.processTicksAndRejections (node:internal/process/task_queues:77:11)\\nfor call at\\n    at ServiceClientImpl.makeUnaryRequest (/app/node_modules/@grpc/grpc-js/build/src/client.js:161:32)\\n    at ServiceClientImpl.\\u003canonymous\\u003e (/app/node_modules/@grpc/grpc-js/build/src/make-client.js:105:19)\\n    at /app/node_modules/@opentelemetry/instrumentation-grpc/build/src/clientUtils.js:131:31\\n    at /app/node_modules/@opentelemetry/instrumentation-grpc/build/src/instrumentation.js:211:209\\n    at AsyncLocalStorage.run (node:async_hooks:346:14)\\n    at AsyncLocalStorageContextManager.with (/app/node_modules/@opentelemetry/context-async-hooks/build/src/AsyncLocalStorageContextManager.js:33:40)\\n    at ContextAPI.with (/app/node_modules/@opentelemetry/api/build/src/api/context.js:60:46)\\n    at ServiceClientImpl.clientMethodTrace [as getAds] (/app/node_modules/@opentelemetry/instrumentation-grpc/build/src/instrumentation.js:211:42)\\n    at /app/.next/server/pages/api/data.js:1:1024\\n    at new ZoneAwarePromise (/app/node_modules/zone.js/bundles/zone.umd.js:1340:33)\"}}]}],\"status\":{\"code\":2}}]},{\"scope\":{\"name\":\"@opentelemetry/instrumentation-http\",\"version\":\"0.52.1\"},\"spans\":[{\"traceId\":\"a3068c5690d7e955872ea04eb2f2859b\",\"spanId\":\"2179d960e903d030\",\"parentSpanId\":\"749576475bfd303f\",\"name\":\"GET\",\"kind\":2,\"startTimeUnixNano\":\"1724248066952000000\",\"endTimeUnixNano\":\"1724248066960664662\",\"attributes\":[{\"key\":\"http.url\",\"value\":{\"stringValue\":\"http://frontend-proxy:8080/api/data?contextKeys=assembly\"}},{\"key\":\"http.host\",\"value\":{\"stringValue\":\"frontend-proxy:8080\"}},{\"key\":\"net.host.name\",\"value\":{\"stringValue\":\"frontend-proxy\"}},{\"key\":\"http.method\",\"value\":{\"stringValue\":\"GET\"}},{\"key\":\"http.scheme\",\"value\":{\"stringValue\":\"http\"}},{\"key\":\"http.target\",\"value\":{\"stringValue\":\"/api/data?contextKeys=assembly\"}},{\"key\":\"http.user_agent\",\"value\":{\"stringValue\":\"python-requests/2.31.0\"}},{\"key\":\"http.flavor\",\"value\":{\"stringValue\":\"1.1\"}},{\"key\":\"net.transport\",\"value\":{\"stringValue\":\"ip_tcp\"}},{\"key\":\"net.host.ip\",\"value\":{\"stringValue\":\"172.18.0.23\"}},{\"key\":\"net.host.port\",\"value\":{\"intValue\":\"8080\"}},{\"key\":\"net.peer.ip\",\"value\":{\"stringValue\":\"172.18.0.25\"}},{\"key\":\"net.peer.port\",\"value\":{\"intValue\":\"60168\"}},{\"key\":\"http.status_code\",\"value\":{\"intValue\":\"500\"}},{\"key\":\"http.status_text\",\"value\":{\"stringValue\":\"INTERNAL SERVER ERROR\"}}],\"status\":{\"code\":2}}]}]}]}\n에러가 왜나는지 알려줄 수 있니?\n"}
# # agentic_workflow_data = {}
# json_data = json.dumps(prompt_data)
# headers = {
#     "X-API-KEY": api_key,
#     "content-type": "application/json"
# }
#
# response = requests.post(url, data=json_data, headers=headers)
# print(response)
# print(response.text)


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
    data = data.replace("{{error_log}}",log_data)
    data = data.replace("{{error_span}}",span_data)
    data = {"message":data}
    json_data = json.dumps(data)
    return json_data

# 오류 리포트 생성
def create_error_report(log_data, span_data):

    json_data = create_message(log_data, span_data)
    result = call_freesia_api(json_data)
    print(result.text)

#create_error_report(log_data,span_data)
##
log_data = """{
    "container.id": "3664da43153e5051d2c104b66787eed90be022efd5f3d45eec9b9a4e47b4c718",
    "os.description": "Linux 5.15.153.1-microsoft-standard-WSL2",
    "process.command_line": "/opt/java/openjdk/bin/java -javaagent:/usr/src/app/opentelemetry-javaagent.jar oteldemo.AdService",
    "service.name": "adservice",
    "telemetry.sdk.language": "java",
    "logRecords_severityText": "WARN",
    "logRecords_body_stringValue": "GetAds Failed with status Status{code=UNAVAILABLE, description=null, cause=null}",
    "traceId": "a3068c5690d7e955872ea04eb2f2859b",
    "observedTimeUnixNano": "2024-08-21 22:47:46"
}"""
span_data = """{
    "service.name": "adservice",
    "os.type": "linux",
    "traceId": "a3068c5690d7e955872ea04eb2f2859b",
    "spanId": "510b715ab6375846",
    "name": "oteldemo.AdService/GetAds",
    "http.status_code": null,
    "rpc.grpc.status_code": "14",
    "exception.message": "UNAVAILABLE",
    "exception.stacktrace": null,
    "http.url": null,
    "rpc.method": "GetAds",
    "startTimeUnixNano": "2024-08-21 22:47:46",
    "endTimeUnixNano": "2024-08-21 22:47:46"
},
{
    "service.name": "frontend",
    "os.type": "linux",
    "traceId": "a3068c5690d7e955872ea04eb2f2859b",
    "spanId": "428b07968ae20727",
    "name": "grpc.oteldemo.AdService/GetAds",
    "http.status_code": null,
    "rpc.grpc.status_code": "14",
    "exception.message": null,
    "exception.stacktrace": null,
    "http.url": null,
    "rpc.method": "GetAds",
    "startTimeUnixNano": "2024-08-21 22:47:46",
    "endTimeUnixNano": "2024-08-21 22:47:46"
},
{
    "service.name": "frontend",
    "os.type": "linux",
    "traceId": "a3068c5690d7e955872ea04eb2f2859b",
    "spanId": "d242dc005baabd8f",
    "name": "executing api route (pages) /api/data",
    "http.status_code": "500",
    "rpc.grpc.status_code": null,
    "exception.message": "14 UNAVAILABLE: ",
    "exception.stacktrace": "Error: 14 UNAVAILABLE: \n    at callErrorFromStatus (/app/node_modules/@grpc/grpc-js/build/src/call.js:31:19)\n    at Object.onReceiveStatus (/app/node_modules/@grpc/grpc-js/build/src/client.js:193:76)\n    at Object.onReceiveStatus (/app/node_modules/@grpc/grpc-js/build/src/client-interceptors.js:360:141)\n    at Object.onReceiveStatus (/app/node_modules/@grpc/grpc-js/build/src/client-interceptors.js:323:181)\n    at /app/node_modules/@grpc/grpc-js/build/src/resolving-call.js:129:78\n    at process.processTicksAndRejections (node:internal/process/task_queues:77:11)\nfor call at\n    at ServiceClientImpl.makeUnaryRequest (/app/node_modules/@grpc/grpc-js/build/src/client.js:161:32)\n    at ServiceClientImpl.<anonymous> (/app/node_modules/@grpc/grpc-js/build/src/make-client.js:105:19)\n    at /app/node_modules/@opentelemetry/instrumentation-grpc/build/src/clientUtils.js:131:31\n    at /app/node_modules/@opentelemetry/instrumentation-grpc/build/src/instrumentation.js:211:209\n    at AsyncLocalStorage.run (node:async_hooks:346:14)\n    at AsyncLocalStorageContextManager.with (/app/node_modules/@opentelemetry/context-async-hooks/build/src/AsyncLocalStorageContextManager.js:33:40)\n    at ContextAPI.with (/app/node_modules/@opentelemetry/api/build/src/api/context.js:60:46)\n    at ServiceClientImpl.clientMethodTrace [as getAds] (/app/node_modules/@opentelemetry/instrumentation-grpc/build/src/instrumentation.js:211:42)\n    at /app/.next/server/pages/api/data.js:1:1024\n    at new ZoneAwarePromise (/app/node_modules/zone.js/bundles/zone.umd.js:1340:33)",
    "http.url": null,
    "rpc.method": null,
    "startTimeUnixNano": "2024-08-21 22:47:46",
    "endTimeUnixNano": "2024-08-21 22:47:46"
},
{
    "service.name": "frontend",
    "os.type": "linux",
    "traceId": "a3068c5690d7e955872ea04eb2f2859b",
    "spanId": "2179d960e903d030",
    "name": "GET",
    "http.status_code": "500",
    "rpc.grpc.status_code": null,
    "exception.message": null,
    "exception.stacktrace": null,
    "http.url": "http://frontend-proxy:8080/api/data?contextKeys=assembly",
    "rpc.method": null,
    "startTimeUnixNano": "2024-08-21 22:47:46",
    "endTimeUnixNano": "2024-08-21 22:47:46"
},
{
    "service.name": "loadgenerator",
    "os.type": null,
    "traceId": "a3068c5690d7e955872ea04eb2f2859b",
    "spanId": "2ecda53ce636e5ce",
    "name": "GET",
    "http.status_code": "500",
    "rpc.grpc.status_code": null,
    "exception.message": null,
    "exception.stacktrace": null,
    "http.url": "http://frontend-proxy:8080/api/data/?contextKeys=assembly",
    "rpc.method": null,
    "startTimeUnixNano": "2024-08-21 22:47:46",
    "endTimeUnixNano": "2024-08-21 22:47:46"
}"""
# create_error_report(log_data, span_data)

