import threading
from batch import trace_batch, log_batch
import psycopg2
import re

trace_ids_dict = {}

# 각 batch를 실행할 스레드를 생성
thread1 = threading.Thread(target=log_batch.run_batch1(), args=(trace_ids_dict, ))
thread2 = threading.Thread(target=trace_batch.run_batch2(), args=(trace_ids_dict, ))

# 스레드를 시작 (동시에 실행)
thread1.start()
thread2.start()


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
            # error_solution_match = re.search(r"조치방안\*\*:\s*([^\n]+)", content)

            service_code = service_code_match.group(1) if service_code_match else None
            error_name = error_name_match.group(1) if error_name_match else None
            error_content = error_content_match.group(1) if error_content_match else None
            error_location = error_location_match.group(1) if error_location_match else None
            error_cause = error_cause_match.group(1) if error_cause_match else None
            # error_solution = error_solution_match.group(1) if error_solution_match else None

            data["service_code"] = service_code
            data["error_name"] = error_name
            data["error_content"] = error_content
            data["error_location"] = error_location
            data["error_cause"] = error_cause
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
        # "error_solution": dbdata['error_solution']
    }
    # SQL 쿼리 생성 및 실행
    insert_query = """
            INSERT INTO error_report (
                service_code, error_name, error_content, error_location, error_cause
            ) VALUES (%s, %s, %s, %s, %s)
        """
    try:
        cursor.execute(insert_query, (
            data_to_insert["service_code"],
            data_to_insert["error_name"],
            data_to_insert["error_content"],
            data_to_insert["error_location"],
            data_to_insert["error_cause"]
            # data_to_insert["error_solution"]
        ))

        # 변경사항 저장
        connection.commit()
    finally:
        connection.close()


# conn, cur = db_connection()
# db_data = make_db_data()
# print(db_data)
# insert_data(conn, cur, db_data)
# select_data(conn, cur)



