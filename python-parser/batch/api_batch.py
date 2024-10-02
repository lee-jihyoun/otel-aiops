import configparser
import json
import logging
import redis
import time
from report_util.create_report import CreateReport


def get_redis_db_connection():
    config = configparser.ConfigParser()
    config.read('./config/db_config.ini')
    host = config['redis-DB']['DB_HOST']
    port = config['redis-DB']['DB_PORT']
    pwd = config['redis-DB']['DB_PWD']
    db_num = config['redis-DB']['DB']
    conn = redis.Redis(host=host, port=port, decode_responses=True, db=db_num, password=pwd)
    return conn


def get_complete_parsing_data(r, key):
    if key is None:
        logging.info("* key가 없습니다.")
        return None, None
    else:
        hash_key = "complete_hash:" + key
        parsing_log = r.hget(hash_key, "parsing_data_log")
        parsing_trace = r.hget(hash_key, "parsing_data_trace")
        if parsing_log is None or parsing_trace is None:
            logging.warning(f"Key {key}에 대한 파싱 데이터가 없습니다.")
            return None, None
        else:
            # list로 변환
            parsing_log = json.loads(parsing_log)
            parsing_trace = json.loads(parsing_trace)
            return parsing_log, parsing_trace


def delete_key(r, key):
    if key is not None:
        all_store = ["complete_hash", "complete_key_store", "key_store", "filtered_log_list", "filtered_trace_list", "original_log_list", "original_trace_list", "fail_key_store"]
        try:
            for store in all_store:
                del_key = store + ":" + key
                r.delete(del_key)
                logging.info(f"메일 발송을 성공하여 모든 hash와 list에서 {key}를 삭제했습니다.")
        except KeyError as e:
            logging.error(f"* 모든 hash와 list에서 key를 삭제하던 중 key가 없어 오류가 발생했습니다.: {e}")


def process_creating_report(r, report, key):
    # complete_hash에서 key에 해당하는 파싱 데이터 꺼내기
    log, trace = get_complete_parsing_data(r, key)
    if log is None or trace is None:
        logging.warning(f"Key {key}에 대한 파싱 데이터가 없습니다.")
        return
    else:
        # DB error_history에 중복이 있는지 체크
        is_duplicate = report.is_duplicate_error(trace)
        # DB error_report에 이미 발송된 적이 있는 traceId 인지 체크
        is_exists = report.is_exists_key_from_error_report(key)
        if is_duplicate is False:
            if is_exists is False:
                # 오류리포트 생성 및 저장
                is_success = report.is_success_create_and_save_error_report(key, log, trace)
                if is_success is True:
                    # DB insert 성공 시 모든 hash와 list에서 키 삭제
                    logging.info(f"* DB insert에 성공하여 모든 hash와 list에서 {key}를 삭제합니다.")
                    delete_key(r, key)
                elif is_success is False:
                    # 메일 발송 실패하면 fail_key_store에 rpush
                    r.rpush("fail_key_store", key)
                    logging.info(f"* fail_key_store에 추가된 키 {key}")
            else:
                logging.warning("* 이미 메일이 발송된 traceId 입니다.")


def main():
    r = get_redis_db_connection()
    # CreateReport 클래스 인스턴스 생성
    report = CreateReport()
    while True:
        logging.info(f"************* api_batch start *************")

        # complete_key_store에서 key 꺼내기
        logging.info(f"* 현재 complete_key_store의 길이: {r.llen('complete_key_store')}")
        complete_key = r.lpop("complete_key_store")
        if complete_key is not None:
            logging.info(f"* --------------- 현재 complete_key는 {complete_key} ---------------")
            process_creating_report(r, report, complete_key)
        else:
            logging.warning("* complete_key_store에 key가 없습니다.")

        # fail_key_store에서 key 꺼내기
        fail_key = r.lpop("fail_key_store")
        if fail_key is not None:
            logging.info(f"* --------------- 현재 fail_key는 {fail_key} ---------------")
            process_creating_report(r, report, fail_key)
        else:
            logging.warning("* fail_key_store에 key가 없습니다.")

        time.sleep(15) # 15초