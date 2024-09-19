import psycopg2  # pip install psycopg2-binary
import requests
import json
import re


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

    # DB 연결 설정
    def db_connection(self):

        return psycopg2.connect(
            host='100.83.227.59',
            port=5532,
            user='test_admin',
            password='new1234!',
            database='rnp'

            # 집 서버
            # host='192.168.55.125',
            # port=5532,
            # user='test_admin',
            # password='rlatjdcjf!1',
            # database='rnp'
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
        # print(result.text)
        return result.text



    # DB에서 error_history 읽어오기
    def select_error_history(self, service_code, exception_stacktrace):
        with self.db_connection() as conn, conn.cursor() as cur:
            read_query = f"""
                SELECT * FROM error_history AS eh
                WHERE eh.create_time > now() - '1 day'::interval
                AND eh.service_code = '{service_code}'
                AND eh.exception_stacktrace = '{exception_stacktrace}'
            """
            cur.execute(read_query)
            result = cur.fetchall()
        return result

    # DB에서의 error_history와 완료 목록을 비교
    def compare_db_dict(self, complete_dict):
        error_report_dict ={}
        # 여기서 단위서비스코드, 오류내용, 시간 세개 조건으로 추가해야함
        for key, value in complete_dict.items():
            result = self.select_error_history(value["service_code"], value["exception_stacktrace"])
            # print(type(result))
            # 비교 데이터 데이터 없음
            if len(result)==0 :
                error_report_dict[key] = value
            else:
                print('* DB insert 실패. 중복된 exception.stacktrace가 존재합니다.')
        return error_report_dict

    # 오류 리포트 생성 및 데이터베이스에 데이터 insert
    def create_and_save_error_report(self, error_report_dict):
        for key, value in error_report_dict.items():
            value["parsing_data_log"] = self.remove_json_value(value["parsing_data_log"])
            response = self.create_error_report(value["parsing_data_log"], value["parsing_data_trace"])
            clean_result = self.make_clean_markdown_json(response)
            db_data = self.make_db_data(clean_result)
            db_data["trace_id"] = key
            self.save_error_report(db_data)
            self.save_error_history(value)
            print("* DB insert 완료")

    # error_history 테이블에 데이터 추가
    def save_error_history(self, error_report):
        with self.db_connection() as conn, conn.cursor() as cur:
            cur.execute('''
                INSERT INTO error_history (service_code, exception_stacktrace)
                VALUES (%s, %s)
            ''', (error_report["service_code"], error_report["exception_stacktrace"]))

    def save_error_report(self, error_report):
        with self.db_connection() as conn, conn.cursor() as cur:
            cur.execute('''
                INSERT INTO error_report (
                    service_code,
                    error_name,
                    error_content,
                    error_create_time,
                    error_location,
                    error_cause,
                    error_solution,
                    trace_id,
                    service_impact)
                VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)
            ''', (
                    error_report["service_code"],
                    error_report["error_name"],
                    error_report["error_content"],
                    error_report["error_create_time"],
                    error_report["error_location"],
                    error_report["error_cause"],
                    error_report["error_solution"],
                    error_report["trace_id"],
                    error_report["service_impact"]
            ))

    # 리포트 대상 데이터 출력
    # 전역변수 main_dcit를 사용하려고 했는데,, 순환 참조.
    def findCompleteData(self, main_dict):
        # status
        #     log : 로그파싱 완료 상태
        #     trace : 트레이스 파싱 완료 상태
        #     confirm : 1차 파싱 완료 상태 (이상태에서 한번 더 실행하면 complete 로 변경됨)
        #     complete : 2차 파싱 완료 상태 (모든 데이터 파싱 완료 상태)
        # parsing_data_log : 파싱된 로그
        # parsing_data_trace : 파싱된 트레이스
        # retry : 리트라이횟수
        # mail : 메일 발송 여부
        # service_code : 서비스코드
        # exception_stacktrace : 오류로그 두줄
        complete_dict={}


        for key, value in main_dict.items():
            if value["mail"] == "N" and value["status"] == "complete":
                complete_dict[key] = value
        return complete_dict

    # Database insert 데이터로 변환
    def make_db_data(self, clean_response):
        content = clean_response['data']['content']
        error_report = {}
        service_code = content["기본정보"]["서비스코드"]
        error_name = content["오류내용"]["오류 이름"]
        error_create_time = content["오류내용"]["발생 시간"]
        error_content = content["오류내용"]["오류 내용"]
        error_location = content["분석결과"]["오류 발생 위치"]
        error_cause = content["분석결과"]["오류 근본 원인"]
        service_impact = content["분석결과"]["서비스 영향도"]
        error_solution = content["후속조치"]["조치방안"]

        error_report["service_code"] = service_code
        error_report["error_name"] = error_name
        error_report["error_create_time"] = error_create_time
        error_report["error_content"] = error_content
        error_report["error_location"] = error_location
        error_report["error_cause"] = error_cause
        error_report["service_impact"] = service_impact
        error_report["error_solution"] = error_solution
        return error_report

    # log data에 포함된 {} 기호 전처리
    def remove_json_value(self, value):
        # print('* in remove_json_value 함수:', value)
        value = value.replace("{", "(").replace("}", ")")
        return value

    # response에 마크다운이 포함된 경우 escape 문자열 처리
    def make_clean_markdown_json(self, markdown_json):
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