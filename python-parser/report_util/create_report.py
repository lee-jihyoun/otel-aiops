import logging

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
    def create_message(self, log, trace):
        # 템플릿을 그대로 사용
        global template
        # list -> str로 변환
        log = json.dumps(log)
        trace = json.dumps(trace)

        data = template[:].replace("{{error_log}}", log)
        data = data.replace("{{error_span}}", trace)
        data = {"message": data}
        return json.dumps(data)

    # 오류 리포트 생성
    def create_error_report(self, log, trace):
        json_data = self.create_message(log, trace)
        result = self.call_freesia_api(json_data)
        # print(result.text)
        return result.text

    # DB에서 error_history 읽어오기
    def select_error_history(self, service_code, exception_stacktrace_short):
        print("* select 하려는 service_code:", service_code)
        with self.db_connection() as conn, conn.cursor() as cur:
            read_query = f"""
                SELECT * FROM error_history AS eh
                WHERE eh.create_time > now() - '1 day'::interval
                AND eh.service_code = '{service_code}'
                AND eh.exception_stacktrace_short = '{exception_stacktrace_short}'
            """
            cur.execute(read_query)
            result = cur.fetchall()
        return result

    # DB에서의 error_history와 완료 목록을 비교(중복 체크)
    def is_duplicate_error(self, key, trace_data):
        logging.info("* 중복된 오류가 있었는지 확인합니다.")
        duplicate_cnt = 0
        for trace in trace_data:
            # str -> list로 변환
            trace_list = json.loads(trace)
            # dict에 접근
            for trace_dict in trace_list:
                # TODO: service_code를 잡을때 exception.stacktrace.short가 겹치는 부분의 code는 F10011 / freesia 결과로 잡히는 code는 CA1003 -> error_report, error_history에는 CA1002으로 들어가니까 중복체크를 못함.
                service_code = trace_dict.get("service.code")
                exception_stacktrace_short = trace_dict.get("exception.stacktrace.short")
                # print(exception_stacktrace_short)
                result = self.select_error_history(service_code, exception_stacktrace_short)
                if len(result) != 0:
                    duplicate_cnt += 1

        if duplicate_cnt > 0:
            logging.info("* 중복 오류가 있습니다. 오류 보고서를 생성할 수 없습니다")
            return True
        else:
            logging.info("* 중복 오류가 없습니다. 오류 보고서를 생성합니다.")
            return False

    # 오류 리포트 생성 및 데이터베이스에 데이터 insert
    def create_and_save_error_report(self, key, log, trace):
        response = self.create_error_report(log, trace)
        clean_result = self.make_clean_markdown_json(response)
        db_data = self.make_db_data(clean_result)
        if db_data is not None:
            db_data["trace_id"] = key
            logging.info(f"* freesia 오류보고서:\n {db_data}")
            self.save_error_report(db_data)
            self.save_error_history(db_data)
            logging.info("* DB insert 완료")
            return "success"
        else:
            logging.info("* DB insert 실패")
            return "fail"

    # error_history 테이블에 데이터 추가
    def save_error_history(self, error_report):
        with self.db_connection() as conn, conn.cursor() as cur:
            cur.execute('''
                INSERT INTO error_history (service_code, exception_stacktrace_short)
                VALUES (%s, %s)
            ''', (error_report["service_code"], error_report["exception_stacktrace_short"]))

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

    # DB insert 하기 위한 데이터로 변환
    def make_db_data(self, clean_response):
        retry = 0
        max_retry = 5
        while retry < max_retry:
            try:
                content = clean_response['data']['content']
                error_report = {}
                service_code = content["기본정보"]["서비스코드"]
                error_name = content["오류내용"]["오류 이름"]
                error_create_time = content["오류내용"]["발생 시간"]
                error_content = content["오류내용"]["오류 내용"]
                error_location = content["분석결과"]["오류 발생 위치"]
                exception_stacktrace_short = content["분석결과"]["exception.stacktrace.short"]
                error_cause = content["분석결과"]["오류 근본 원인"]
                service_impact = content["분석결과"]["서비스 영향도"]
                error_solution = content["후속조치"]["조치방안"]

                error_report["service_code"] = service_code
                error_report["error_name"] = error_name
                error_report["error_create_time"] = error_create_time
                error_report["error_content"] = error_content
                error_report["error_location"] = error_location
                error_report["exception_stacktrace_short"] = exception_stacktrace_short
                error_report["error_cause"] = error_cause
                error_report["service_impact"] = service_impact
                error_report["error_solution"] = error_solution
                return error_report

            except KeyError as e:
                logging.info(f"* freesia 응답에 key가 없어 오류가 발생했습니다.: {e}")
                logging.info(f"* 다시 시도합니다.")
                retry += 1

        logging.info("* freesia 데이터 생성에 실패했습니다.")
        return None

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