import time
import logging
import redis
import json
from report_util.create_report import CreateReport


def get_complete_parsing_data(r, key):
    if key is None:
        print("* key가 없습니다.")
    try:
        hash_key = "complete_hash:" + key
        parsing_log = r.hget(hash_key, "parsing_data_log")
        parsing_trace = r.hget(hash_key, "parsing_data_trace")

        # list로 변환
        parsing_log = json.loads(parsing_log)
        parsing_trace = json.loads(parsing_trace)
        return parsing_log, parsing_trace
    except TypeError as e:
        print(f"* TypeError: {e}")


def delete_key(r, key):
    if key is not None:
        all_hash = ["complete_hash", "complete_key_store", "key_store", "filtered_log_hash", "filtered_trace_hash", "original_log_hash", "original_trace_hash", "fail_key_store"]
        try:
            for hash in all_hash:
                del_key = hash + ":" + key
                r.delete(del_key)
        except KeyError as e:
            print(e)



def process_creating_report(r, report, key):
    # complete_hash에서 key에 해당하는 파싱 데이터 꺼내기
    log, trace = get_complete_parsing_data(r, key)
    # DB error_history에 중복이 있는지 체크
    is_duplicate = report.is_duplicate_error(trace)
    if is_duplicate is False:
        # 오류리포트 생성 및 저장
        result = report.create_and_save_error_report(key, log, trace)
        if result == "success":
            # DB insert 성공 시 모든 hash에서 키 삭제
            print(f"* DB insert에 성공하여 모든 hash에서 {key}를 삭제합니다.")
            delete_key(r, key)
        elif result == "fail":
            # 메일 발송 실패하면 fail_key_store에 rpush
            r.rpush("fail_key_store", key)
            logging.info(f"* fail_key_store에 추가된 키 {key}")

    # TODO: 이미 발송된 적이 있는가? error_report에 traceId 체크


def main():
    r = redis.Redis(host='100.83.227.59', port=16379, decode_responses=True, db=3, password='redis1234!')
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
            logging.info("* complete_key_store에 key가 없습니다.")

        # fail_key_store에서 key 꺼내기
        fail_key = r.lpop("fail_key_store")
        if fail_key is not None:
            logging.info(f"* --------------- 현재 fail_key는 {fail_key} ---------------")
            process_creating_report(r, report, fail_key)
        else:
            logging.info("* fail_key_store에 key가 없습니다.")

        time.sleep(15) # 15초