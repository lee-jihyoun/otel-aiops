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
        # print("* select 하려는 service_code:", service_code)
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
    def is_duplicate_error(self, trace_data):
        logging.info("* 중복된 오류가 있었는지 확인합니다.")
        duplicate_cnt = 0
        for trace in trace_data:
            # str -> list로 변환
            trace_list = json.loads(trace)
            # dict에 접근
            for trace_dict in trace_list:
                service_code = trace_dict.get("service.code")
                exception_stacktrace_short = trace_dict.get("exception.stacktrace.short")
                # TODO: prompt 수정하기 -> service code와 일치하는 exception.stacktrace 요청하기.
                result = self.select_error_history(service_code, exception_stacktrace_short)
                if len(result) != 0:
                    self.increase_error_history_cnt(service_code, exception_stacktrace_short)
                    duplicate_cnt += 1

        if duplicate_cnt > 0:
            logging.info("* 중복 오류가 있습니다. 오류 보고서를 생성할 수 없습니다")
            return True
        else:
            logging.info("* 중복 오류가 없습니다. 오류 보고서를 생성합니다.")
            return False

    # DB에서의 error_history와 완료 목록을 비교(중복 체크)
    # def is_duplicate_error_after_check(self, freesia_response):
    #     logging.info("* 중복된 오류가 있었는지 확인합니다.")
    #     # 원래꺼
    #     # service_code = freesia_response["data"]["content"]["분석결과"]["서비스코드"]
    #     # exception_stacktrace_short = freesia_response["data"]["content"]["기본정보"]["exception.stacktrace.short"]
    #     # 임시 데이터
    #     service_code = freesia_response["service_code"]
    #     exception_stacktrace_short = freesia_response["exception_stacktrace_short"]
    #     result = self.select_error_history(service_code, exception_stacktrace_short)
    #     if len(result) != 0:
    #         self.increase_error_history_cnt(service_code, exception_stacktrace_short)
    #         logging.info("* 중복 오류가 있습니다. 오류 보고서를 생성할 수 없습니다")
    #         return True
    #     else:
    #         logging.info("* 중복 오류가 없습니다. 오류 보고서를 생성합니다.")
    #         return False

    def increase_error_history_cnt(self, service_code, exception_stacktrace_short):
        with self.db_connection() as conn, conn.cursor() as cur:
            cur.execute('''
                UPDATE error_history
                SET cnt = cnt + 1
                WHERE service_code = %s
                AND exception_stacktrace_short = %s
            ''',
                        (service_code, exception_stacktrace_short))

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

    # def create_and_save_error_report_after_check(self, key, log, trace):
    #     response = self.create_error_report(log, trace)
    #     # str -> dict로 변환
    #     response = json.loads(response)
    #     response_code = response.get("code")
    #     if response_code == "9999":
    #         print("* freeesia 응답 코드가 9999입니다. ")
    #     else:
    #         clean_result = self.make_clean_markdown_json(response)
    #         # clean_result = {'service_code': 'CA1003', 'error_name': 'grpc.oteldemo.CartService/GetCart', 'error_create_time': '2024-09-19 23:40:36', 'error_content': "Error when executing service method '{ServiceMethod}'.", 'error_location': '오류는 프론트엔드 서비스(frontend)에서 grpc.oteldemo.CartService/GetCart 메서드 실행 중 발생하였습니다. stacktrace에서 아래와 같은 에러가 발생하였습니다: Error: 13 INTERNAL: Received RST_STREAM with code 2 triggered by internal client error: Session closed with error code 2 at callErrorFromStatus (/app/node_modules/@grpc/grpc-js/build/src/call.js:31:19)', 'exception_stacktrace_short': 'Error: 13 INTERNAL: Received RST_STREAM with code 2 triggered by internal client error: Session closed with error code 2 at callErrorFromStatus (/app/node_modules/@grpc/grpc-js/build/src/call.js:31:19)', 'error_cause': '1. 프론트엔드 서비스에서 내부 클라이언트 오류로 인해 세션이 닫히면서 에러가 발생하였습니다. 2. 이는 cartservice에서 전파된 문제로, traceId(3c7829d88f923d64d55339655779a249)를 통해 확인할 수 있습니다.', 'service_impact': '장바구니 서비스의 오류로 인해 사용자는 장바구니 정보를 가져올 수 없으며, 이는 쇼핑몰의 기능에 심각한 영향을 미칠 수 있습니다.', 'error_solution': '1. **장바구니 서비스 설정 확인**: - 장바구니 서비스의 로그를 확인하여 내부 클라이언트 오류의 원인을 파악합니다. - 로그 파일은 /var/log/cartservice.log에 위치할 수 있습니다. - 아래 명령어를 사용하여 로그 파일을 확인합니다: tail -f /var/log/cartservice.log 2. **서비스 재시작**: - 문제를 해결한 후 장바구니 서비스를 재시작합니다. 아래 명령어를 사용하여 Docker 컨테이너를 재시작할 수 있습니다: docker restart cartservice 3. **로그 및 모니터링**: - 변경 후, Opentelemetry를 통해 로그와 메트릭을 모니터링하여 동일한 오류가 다시 발생하는지 확인합니다. - 특히, 장바구니 요청과 관련된 로그를 집중적으로 모니터링합니다. 4. **테스트 수행**: - 설정 변경 후 장바구니 기능이 정상적으로 작동하는지 테스트합니다. - 다양한 시나리오를 통해 장바구니 프로세스가 정상적으로 완료되는지 확인합니다.', 'trace_id': '3c7829d88f923d64d55339655779a249'}
    #
    #         is_duplicate = self.is_duplicate_error(clean_result)
    #         if is_duplicate is False:
    #             # 중복이 아닐 경우
    #             db_data = self.make_db_data(clean_result)
    #             if db_data is not None:
    #                 db_data["trace_id"] = key
    #                 logging.info(f"* freesia 오류보고서:\n {db_data}")
    #                 self.save_error_report(db_data)
    #                 self.save_error_history(db_data)
    #                 logging.info("* DB insert 완료")
    #                 return "success"
    #             else:
    #                 logging.info("* DB insert 실패")
    #                 return "fail"

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
                retry += 1
                logging.info(f"* {retry}번째 다시 시도합니다.")

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
