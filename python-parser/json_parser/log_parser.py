import configparser
import itertools
import json
import logging
import redis
from util.datetime_util import change_timenano_format

filter_last_position = 0
original_last_position = 0


class LogParsing:

    def __init__(self, input_path, file_name):

        self.input_path = input_path
        self.file_name = file_name

    def get_redis_db_connection(self):
        config = configparser.ConfigParser()
        config.read('./config/db_config.ini')
        host = config['redis-DB']['DB_HOST']
        port = config['redis-DB']['DB_PORT']
        pwd = config['redis-DB']['DB_PWD']
        db_num = config['redis-DB']['DB']
        conn = redis.Redis(host=host, port=port, decode_responses=True, db=db_num, password=pwd)
        return conn

    def logparser(self):
        input_path = self.input_path
        file_name = self.file_name

        global filter_last_position, original_last_position
        parsing_log_data_list = []

        with open(input_path + file_name, "r") as log_file:

            # logging.info("===========================")
            # logging.info(log_file)

            if file_name == "filtered_logs.json":
                idx = filter_last_position
            else:
                idx = original_last_position

            for current_index, line in enumerate(itertools.islice(log_file, idx, None), start=idx):

                # logging.info("===========================")
                # logging.info(line)

                if not line:  # 더 이상 읽을 데이터가 없으면
                    # logging.info("데이터가 없습니다")
                    break  # 루프를 종료

                else:
                    # logging.info(f"================ filtered_log 파싱 start: {datetime.datetime.now()} ================")

                    try:
                        log_data = json.loads(line.strip())
                        change_timenano_format(log_data)  # 시간 전처리 적용
                        for resource_log in log_data.get('resourceLogs', []):
                            for scope_log in resource_log.get("scopeLogs", []):
                                for log_record in scope_log.get("logRecords", []):
                                    parsed_info = {
                                        "container.id": None,
                                        "os.description": None,
                                        "process.command_line": None,
                                        "service.name": None,
                                        "service.code": None,
                                        "telemetry.sdk.language": None,
                                        "logRecords_severityText": None,
                                        "logRecords_body_stringValue": None,
                                        "traceId": None,
                                        "observedTimeUnixNano": None,  # 새로운 시간 필드 추가
                                    }
                                    if "resource" in resource_log and "attributes" in resource_log["resource"]:
                                        for attribute in resource_log["resource"]["attributes"]:
                                            if attribute["key"] == "container.id":
                                                parsed_info["container.id"] = attribute["value"]["stringValue"]
                                            if attribute["key"] == "os.description":
                                                parsed_info["os.description"] = attribute["value"]["stringValue"]
                                            if attribute["key"] == "process.command_line":
                                                parsed_info["process.command_line"] = attribute["value"]["stringValue"]
                                            if attribute["key"] == "service.name":
                                                parsed_info["service.name"] = attribute["value"]["stringValue"]
                                            if attribute["key"] == "service.code":
                                                parsed_info["service.code"] = attribute["value"]["stringValue"]
                                            if attribute["key"] == "telemetry.sdk.language":
                                                parsed_info["telemetry.sdk.language"] = attribute["value"]["stringValue"]

                                    if "observedTimeUnixNano" in log_record:
                                        parsed_info["observedTimeUnixNano"] = log_record["observedTimeUnixNano"]
                                    if "severityText" in log_record:
                                        parsed_info["logRecords_severityText"] = log_record["severityText"]
                                    if "body" in log_record and "stringValue" in log_record["body"]:
                                        parsed_info["logRecords_body_stringValue"] = log_record["body"]["stringValue"]
                                    if "traceId" in log_record:
                                        parsed_info["traceId"] = log_record["traceId"]
                                        # logging.info(parsed_info)

                                    # traceid가 비어 있을 경우에는 log_record에 저장하지 않음
                                    if "traceId" in log_record and log_record["traceId"]:
                                        parsing_log_data_list.append(parsed_info)

                    except json.JSONDecodeError as e:
                        logging.ERROR(f"Error parsing line: {e}")

                    # logging.info("**************************")
                    # logging.info("parsing_log_data_list\n")
                    # logging.info(parsing_log_data_list)
                    # logging.info("**************************")

                    # 마지막으로 읽은 위치를 업데이트
                    if file_name == "filtered_logs.json":
                        # 파일 포인터를 마지막 읽은 위치로 이동
                        filter_last_position = current_index + 1

                    else:
                        original_last_position = current_index + 1

                # logging.info("============ log 파싱 end ===========\n")
                # logging.info(parsing_log_data_list)

            return parsing_log_data_list

    def redis_insert(self):
        # Redis 클라이언트 설정
        r = self.get_redis_db_connection()

        while True:

            file_name = self.file_name
            parsing_log_data_list = self.logparser()

            # logging.info("*****************")
            # logging.info("parsing_log_data_list\n")
            # logging.info(parsing_log_data_list)
            # logging.info("**************************")

            if parsing_log_data_list != []:

                # logging.info("============ db 삽입 start===========\n")

                # # list 형태로 저장
                for log in parsing_log_data_list:

                    trace_id = log['traceId']
                    retry_count_store = "retry_count_store:" + trace_id

                    if file_name == "filtered_logs.json":
                        # 전체 키는 traceId로 설정
                        key_list = "filtered_log_list:" + trace_id

                    else:
                        # 전체 키는 traceId로 설정
                        key_list = "original_log_list:" + trace_id

                    log = str(log)

                    r.rpush(key_list, log)
                    r.expire(key_list, 60 * 15)  # 60s * 15 = 15m

                    logging.info(f"* key_list: {key_list}")
                    logging.info(f"* log: {log}")

                    r.sadd("key_store",trace_id)
                    # r.rpush("key_store", trace_id)
                    r.expire("key_store", 60 * 15)  # 60s * 15 = 15m

                    logging.info(f"* key_store: {trace_id}")
                    #
                    # r.hset(retry_count_store, "retry", "0")
                    # r.expire(retry_count_store, 60*15)
                    #
                    # logging.info(f"* retry_count_store: {retry_count_store}")