import configparser
import json
import logging
import re
import ast
from json import JSONDecodeError
import psycopg2  # pip install psycopg2-binary
import requests

# 전역 변수 설정
url = "http://freesia.run:8080/openapi/v1/chat"
headers = {
    "X-API-KEY": "",
    "content-type": "application/json"
}


class CreateReport:
    def __init__(self):
        # DB 연결 및 API 키 불러오기
        with self.get_postgres_db_connection() as conn, conn.cursor() as cur:
            self.api_key = self.select_api_key(cur)
            headers["X-API-KEY"] = self.api_key

    def apply_prompt_version(self, prompt_ver):
        with open(f"./prompt/prompt_template_v{prompt_ver}.txt", 'r', encoding='UTF8') as f:
            template = f.read()
            return template

    # DB 연결 설정
    def get_postgres_db_connection(self):
        config = configparser.ConfigParser()
        config.read('./config/db_config.ini')
        host = config['postgres-DB']['DB_HOST']
        port = config['postgres-DB']['DB_PORT']
        db_name = config['postgres-DB']['DB_NM']
        user = config['postgres-DB']['DB_USER']
        pwd = config['postgres-DB']['DB_PWD']
        conn = psycopg2.connect(host=host, port=port, user=user, password=pwd, database=db_name)
        return conn


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
        print("freesia_response:")
        print(response.text)
        return response

    # 보낼 JSON 데이터의 message 생성
    def create_message(self, log, trace, prompt_ver):
        # prompt 버전에 맞게 템플릿 사용
        template = self.apply_prompt_version(prompt_ver)

        # list -> str로 변환
        log = json.dumps(log)
        trace = json.dumps(trace)

        data = template[:].replace("error_log", log)
        data = data.replace("error_span", trace)
        data = {"message": data}
        req = json.dumps(data, ensure_ascii=False, indent=4)
        # print(req)
        return req

    # 오류 리포트 생성
    def create_error_report(self, log, trace, prompt_ver):
        retry = 0
        max_retry = 5

        while retry < max_retry:
            json_data = self.create_message(log, trace, prompt_ver)
            response = self.call_freesia_api(json_data)

            # str -> dict로 변환
            try:
                response_check = response.json()
                response_code = response_check.get("code")
                content = response_check["data"]["content"]
                if response_code == "9999":
                    logging.info("* freeesia 응답 코드가 9999입니다. ")
                elif content == "죄송합니다, 문의하신 내용에 대한 답변을 찾을 수 없습니다.":
                    logging.error(f"* freesia는 정상이지만 답변이 제대로 생성되지 않았습니다.")
                    retry += 1
                    logging.info(f"* {retry}번째 다시 시도합니다.")
                else:
                    return response.text
            except TypeError as e:
                logging.error(f"* freesia API가 비정상 응답입니다. TypeError: {e}")
                return None

        logging.info("* freesia 데이터 생성에 실패했습니다.")

    # DB에서 error_history 읽어오기
    def is_exists_in_error_history(self, service_code, log_exception_stacktrace_short, trace_exception_stacktrace_short):
        # print("* select 하려는 service_code:", service_code)
        with self.get_postgres_db_connection() as conn, conn.cursor() as cur:
            read_query = f"""
                SELECT EXISTS
                (SELECT seq FROM error_history AS eh
                WHERE eh.create_time > now() - '1 day'::interval
                AND eh.service_code = '{service_code}'
                AND eh.log_exception_stacktrace_short = '{log_exception_stacktrace_short}'
                AND eh.trace_exception_stacktrace_short = '{trace_exception_stacktrace_short}')
            """
            # print(read_query)
            cur.execute(read_query)
            result = cur.fetchall()

        return result[0][0]

    def is_exists_key_from_error_report(self, key):
        with self.get_postgres_db_connection() as conn, conn.cursor() as cur:
            read_query = f"""
                SELECT EXISTS
                (SELECT trace_id FROM error_report AS er
                WHERE er.trace_id = '{key}')
            """
            cur.execute(read_query)
            result = cur.fetchall()
        return result[0][0]

    # DB에서의 error_history와 완료 목록을 비교(중복 체크)
    def is_duplicate_error(self, log_data, trace_data):
        logging.info("* 중복된 오류가 있었는지 확인합니다.")
        combined_data = [
            {'type': 'log', 'data': log_data},
            {'type': 'trace', 'data': trace_data}
        ]
        duplicate_cnt = 0

        for entry in combined_data:
            for item in entry['data']:
                if item is None:
                    logging.info(f"* {entry['type']}가 없습니다.")
                    return False
                else:
                    try:
                        item_list = ast.literal_eval(item)

                    except JSONDecodeError as e:
                        # ex) 데이터 타입이 {'key': 'value'} 면 오류가 발생함. -> json 표준으로 변환 필요: {"key": "value"}
                        logging.error(f"* 중복 오류인지 확인하던 중 오류 발생. JSONDecodeError: {e}")
                        continue

                    # 만약 item_list가 리스트가 아니면 리스트로 강제 변환
                    if isinstance(item_list, dict):
                        item_list = [item_list]
                    elif not isinstance(item_list, list):
                        logging.error(f"* {entry['type']}_list가 리스트도 아니고 딕셔너리도 아닙니다. 건너뜁니다.")
                        continue

                    # # dict에 접근
                    # for item_dict in item_list:
                    #     service_code = item_dict.get("service.code")
                    #     log_exception_stacktrace_short = item_dict.get(f"{entry['type']}.log.exception.stacktrace.short")
                    #     trace_exception_stacktrace_short = item_dict.get(f"{entry['type']}.trace.exception.stacktrace.short")
                    #
                    #     # log와 trace 모두 동일한 stacktrace 검증
                    #     result = self.is_exists_in_error_history(service_code, log_exception_stacktrace_short,
                    #                                              trace_exception_stacktrace_short)
                    #     print(result)
                    #     if result is True:
                    #         self.increase_error_history_cnt(service_code, log_exception_stacktrace_short,
                    #                                         trace_exception_stacktrace_short)
                    #         duplicate_cnt += 1

                    for item_dict in item_list:
                        service_code = item_dict.get("service.code")
                        logRecords_body_stringValue = item_dict.get("logRecords_body_stringValue")
                        url_full = item_dict.get("url.full")

                        # log와 trace 모두 동일한 stacktrace 검증
                        result = self.is_exists_in_error_history(service_code, logRecords_body_stringValue,
                                                                 url_full)
                        print(result)
                        if result is True:
                            self.increase_error_history_cnt(service_code, logRecords_body_stringValue,
                                                            url_full)
                            duplicate_cnt += 1

        if duplicate_cnt > 0:
            logging.info("* 중복 오류가 있습니다. 오류 보고서를 생성할 수 없습니다")
            return True
        else:
            logging.info("* 중복 오류가 없습니다. 오류 보고서를 생성합니다.")
            return False

    def increase_error_history_cnt(self, service_code, log_exception_stacktrace_short, trace_exception_stacktrace_short):
        with self.get_postgres_db_connection() as conn, conn.cursor() as cur:
            # cur.execute('''
            #     UPDATE error_history
            #     SET cnt = cnt + 1
            #     WHERE service_code = %s
            #     AND log_exception_stacktrace_short = %s
            #     AND trace_exception_stacktrace_short = %s
            # ''',
            # (service_code, log_exception_stacktrace_short, trace_exception_stacktrace_short))
            #
            #

            update_query = f"""
                UPDATE error_history
                SET cnt = cnt + 1
                WHERE service_code = '{service_code}'
                AND log_exception_stacktrace_short = '{log_exception_stacktrace_short}'
                AND trace_exception_stacktrace_short = '{trace_exception_stacktrace_short}'
            """
            print(update_query)
            cur.execute(update_query)

    # 오류 리포트 생성 및 데이터베이스에 데이터 insert
    def is_success_create_and_save_error_report(self, key, log, trace, prompt_ver):
        try:
            response = self.create_error_report(log, trace, prompt_ver)
            clean_result = self.make_clean_markdown_json(response)
            db_data = self.make_db_data(clean_result)
            if db_data is not None:
                db_data["trace_id"] = key
                self.save_error_report(db_data)
                self.save_error_history(db_data)
                logging.info(f"* freesia 오류보고서:\n {db_data}")
                logging.info("* DB insert 완료")
                return True
            else:
                logging.info("* DB insert 실패")
                return False
        except TypeError as e:
            logging.info("* freesia 응답이 제대로 생성되지 않았습니다.")
            '''
            freesia에서 이런식으로 응답이 오면 예외로 빠짐.
            {"code":"0000","message":"SUCCESS","data":{"runId":"run-9c8d0660-1358-494f-9518-378b4189aaf0-0",
            "content":"죄송하지만, 제공된 정보가 없어서 오류 보고서를 작성할 수 없습니다. 오류 로그(error_log)와 오류 스팬(error_span)을 제공해 주시면 해당 정보를 기반으로 오류 보고서를 작성해 드리겠습니다.","chatMemoryId":"9c0306de-e109-44f7-9db0-0043f4a6d1f8",
            "promptTokens":1775,"completionTokens":47,"totalTokens":1822,"turnId":"14331149-fb9a-4728-9b9b-c2e82544c5e5",
            "reference":[{"fileId":664,"fileName":"dspace_rag.pdf","page":2,"score":0.5755939149251456,
            "content":"-**특징 **:-PortalCI를 통해 생성된 CI 프로젝트를 관리.-API를 통해 PortalCI와 연동.-Keycloak으로 인증 관리 ####**JenkinsCD**-**역할**:CD(ContinuousDeployment)프로세스 담당. -빌드된 소스 코드를 배포.-**특징 **:-PortalCD에서 API를 통해 생성 및 관리됨.-Keycloak으로 인증 관리 ####**GitLab**-**역할**:소스코드저장소및형상관리.-**특징 **:-PortalCI와 연동하여 프로젝트 생성 및 관리.-Keycloak으로 인증 관리 ####**Jira**-**역할**:이슈및프로젝트관리도구.-**특징 **:-PortalCI에서 생성된 프로젝트에 포함되어 API로 연동.-사용자 요청에 따라 프로젝트 관리 가능.-Keycloak으로 인증 관리 ####**Confluence**-"},{"fileId":664,"fileName":"dspace_rag.pdf","page":5,"score":0.6116485911084105,"content":"[Dev-Space 기능 설명]#포탈프로젝트생성포탈에서프로젝트생성시JIRA,Gitlab,JenkinsCI,JenkinsCD를 각각 생성할 수 있음 JIRA,Gitlab,JenkinsCI의 CRUD는 portalCI에서 담당하고 JenkinsCD의 CRUD는 portalCD에서 담당함-생성 시 데이터 흐름 1. 사용자가 포탈 프로젝트 정보, 생성하려는 Jira,JenkinsCI,JenkinsCD,Gitlab 정보 입력 후생 성 버튼 클릭 2. 포탈 데이터베이스에 포탈 프로젝트 정보 저장 3. 각각 Jira,JenkinsCI,JenkinsCD,Gitlab들을 API를 사용하여 프로젝트 생성 Jira,JenkinsCI,JenkinsCD,Gitlab는 필수 생성이 아님 4.Jira,JenkinsCI,JenkinsCD,Gitlab이 생성 완료되면 포탈 데이터베이스에 생성된 Jira,JenkinsCI,JenkinsCD,Gitlab의 key 또는 ID 값을 저장 5.Jira,JenkinsCI,JenkinsCD,Gitlab 생성 실패 시 실패한 툴에 대한 데이터를 제외한 나머지 툴 데이터를 포탈 데이터베이스에 저장#포탈프로젝트조회포탈에서프로젝트조회시해당프로젝트ID에매핑되어있는JIRA,Gitlab,JenkinsCI,JenkinsCD의 key 또는 ID 값으로 같이 조회 가능 JIRA,Gitlab,JenkinsCI의 조회는 portalCI에서 담당하고 JenkinsCD의 조회는 portalCD에서 담당함 -조회시 데이터 흐름 1. 사용자가 포탈에서 프로젝트 조회 2. 포탈 데이터베이스에서 해당 프로젝트에 연관되어 있는 Jira,JenkinsCI,JenkinsCD,Gitlab 데이터 검색 3. 검색된 Jira,JenkinsCI,JenkinsCD,Gitlab들의 key 또는 ID로 각각의 툴에 API를 호출하여 상세 내용 조회 4. 조회된 내용을 포탈에서 확인"}],"speaker":"dspace_poc_rag","ragDocumentId":75}}
            '''
            return False

    # error_history 테이블에 데이터 추가
    def save_error_history(self, error_report):
        with self.get_postgres_db_connection() as conn, conn.cursor() as cur:
            cur.execute('''
                INSERT INTO error_history (service_code, service_code_sub, log_exception_stacktrace_short, trace_exception_stacktrace_short)
                VALUES (%s, %s, %s, %s)
            ''', (error_report["service_code"],
                  error_report["service_code_sub"],
                  error_report["log_exception_stacktrace_short"],
                  error_report["trace_exception_stacktrace_short"]))

    def save_error_report(self, error_report):
        with self.get_postgres_db_connection() as conn, conn.cursor() as cur:
            cur.execute('''
                INSERT INTO error_report (
                    service_code,
                    service_code_sub,
                    error_name,
                    error_content,
                    error_create_time,
                    error_location,
                    error_cause,
                    error_solution,
                    trace_id,
                    service_impact)
                VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
            ''', (
                    error_report["service_code"],
                    error_report["service_code_sub"],
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
        try:
            content = clean_response['data']['content']
            error_report = {}
            service_code = content["기본정보"]["상위서비스코드"]
            service_code_sub = content["기본정보"]["하위서비스코드"]
            error_name = content["오류내용"]["오류이름"]
            error_create_time = content["오류내용"]["발생시간"]
            error_content = content["오류내용"]["오류내용"]
            error_location = content["분석결과"]["오류발생위치"]
            log_exception_stacktrace_short = content["분석결과"]["log.exception.stacktrace.short"]
            trace_exception_stacktrace_short = content["분석결과"]["trace.exception.stacktrace.short"]
            error_cause = content["분석결과"]["오류근본원인"]
            service_impact = content["분석결과"]["서비스영향도"]
            error_solution = content["후속조치"]["조치방안"]

            error_report["service_code"] = service_code
            error_report["service_code_sub"] = service_code_sub
            error_report["error_name"] = error_name
            error_report["error_create_time"] = error_create_time
            error_report["error_content"] = error_content
            error_report["error_location"] = error_location
            error_report["log_exception_stacktrace_short"] = log_exception_stacktrace_short
            error_report["trace_exception_stacktrace_short"] = trace_exception_stacktrace_short
            error_report["error_cause"] = error_cause
            error_report["service_impact"] = service_impact
            error_report["error_solution"] = error_solution
            return error_report

        except KeyError as e:
            logging.error(f"* freesia 응답에 key가 없어 오류가 발생했습니다.: {e}")

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
            return freesia_result
        except json.JSONDecodeError as e:
            print("* JSON 디코딩 에러:", e)
            print("* 문제 있는 문자열 주변:", cleaned_str[max(0, e.pos-60):e.pos+60])
            print("============== api result DB insert 실패 ==============")

