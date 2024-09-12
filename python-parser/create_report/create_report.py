import psycopg2  # pip install psycopg2-binary
import requests
import json

# 전역 변수 설정
url = "http://freesia.run:8080/openapi/v1/chat"
headers = {
    "X-API-KEY": "",
    "content-type": "application/json"
}
template = ""

class CreateReport:
    def __init__(self):
        global template
        # 템플릿 파일을 읽어 초기화 시 한 번만 저장
        with open("./prompt_template.txt", 'r', encoding='UTF8') as f:
            template = f.read()

        # DB 연결 및 API 키 불러오기
        with self.db_connection() as conn, conn.cursor() as cur:
            self.api_key = self.select_api_key(cur)
            headers["X-API-KEY"] = self.api_key

    def db_connection(self):
        # DB 연결 설정
        return psycopg2.connect(
            host='100.83.227.59',
            port=5532,
            user='test_admin',
            password='new1234!',
            database='rnp'
        )

    # DB에서 API key 읽어오기
    def select_api_key(self, cursor):
        read_query = """
            SELECT api_service_token
            FROM api_auth_tokens
            WHERE api_service_name = 'freesia_api'
        """
        cursor.execute(read_query)
        result = cursor.fetchone()
        return result[0] if result else None

    # 프리지아 API 호출
    def call_freesia_api(self, json_data):
        response = requests.post(url, data=json_data, headers=headers)
        return response

    # 보낼 JSON 데이터의 message 생성
    def create_message(self, log_data, span_data):
        global template
        # 템플릿을 그대로 사용
        data = template[:].replace("{{error_log}}", log_data)
        data = data.replace("{{error_span}}", span_data)
        data = {"message": data}
        return json.dumps(data)

    # 오류 리포트 생성
    def create_error_report(self, log_data, span_data):
        json_data = self.create_message(log_data, span_data)
        result = self.call_freesia_api(json_data)
        print(result.text)

    # DB에서 error_history 읽어오기
    def select_error_history(self):
        with self.db_connection() as conn, conn.cursor() as cur:
            read_query = """
                SELECT * FROM error_history AS eh
                WHERE eh.create_time > now() - '1 day'::interval;
            """
            cur.execute(read_query)
            result = cur.fetchone()
        return result


    def findCompleteData(self):
        a123={
            "status" : "log",
            "parsing_data_log" : "파싱된 로그 456",
            "parsing_data_trace" : "파싱된 트레이스 456",
            "retry" : 1,
            "mail":"N"
        }
        b456={
            "status" : "trace",
            "parsing_data_log" : "파싱된 로그 789",
            "parsing_data_trace" : "파싱된 트레이스 789",
            "retry" : 1,
            "mail":"N"
        }
        c789={
            "status" : "confirm",
            "parsing_data_log" : "파싱된 로그 012",
            "parsing_data_trace" : "파싱된 트레이스 012",
            "retry" : 1,
            "mail":"N"
        }
        d012={
            "status" : "complete",
            "parsing_data_log" : "파싱된 로그 123",
            "parsing_data_trace" : "파싱된 트레이스 123",
            "retry" : 1,
            "mail":"N"
        }
        main_dict={"a123" : a123 , "b456" : b456 , "c789" : c789 , "d012" : d012 }
        for key, value in main_dict.items():
            print(f"Key: {key}")
            for inner_key, inner_value in value.items():
                print(f"  {inner_key}: {inner_value}")
                print(value[inner_key])



        # main_dict = {
        #     "a123": {
        #         "status": "log, trace, confirm(확인), complete(퀄리티 확보 완료상태)",
        #         "parsing_data_log": "로그 파싱된 데이터",
        #         "parsing_data_trace": "트레이스 파싱된 데이터",
        #         "retry": 2,
        #         "mail": "Y"
        #     },
        #     "b123": {
        #         "status": "log, trace, confirm(확인), complete(퀄리티 확보 완료상태)",
        #         "parsing_data_log": "로그 파싱된 데이터",
        #         "parsing_data_trace": "트레이스 파싱된 데이터",
        #         "retry": 2,
        #         "mail": "N"
        #     },
        #     "c123": {
        #         "status": "log, trace, confirm(확인), complete(퀄리티 확보 완료상태)",
        #         "parsing_data_log": "로그 파싱된 데이터",
        #         "parsing_data_trace": "트레이스 파싱된 데이터",
        #         "retry": 2,
        #         "mail": "N"
        #     }
        # }