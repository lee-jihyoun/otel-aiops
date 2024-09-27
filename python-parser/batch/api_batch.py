import time
import logging
import redis
import json

from report_util.create_report import CreateReport


# cd otel_aiops\python-parser
# python -m batch.api_batch

main_dict={}

## 연동 테스트 시 사용
# main_dict = trace_id.main_dict

r = redis.Redis(host='100.83.227.59', port=16379, decode_responses=True, db=5, password='redis1234!')

# 테스트 데이터 삽입
def test_data_set():
    a_log_list = ["log_aaaaaaaaaaaaaaaaaaaa11111111111" , "log_aaaaaaaaaaaaaaaaaaaa22222222222222222"]
    a_trace_list = ["trace_aaaaaaaaaaaaaaaaaaaa1111111111111111" , "trace_aaaaaaaaaaaaaaaaaaaa2222222222222222"]
    a_log_list = json.dumps(a_log_list, ensure_ascii=False).encode('utf-8')
    a_trace_list = json.dumps(a_trace_list, ensure_ascii=False).encode('utf-8')

    r.hset("complete_hash:a123", "parsing_data_log", a_log_list)
    r.hset("complete_hash:a123", "parsing_data_trace", a_trace_list)

    b_log_list = ["log_bbbbbbbbbbbbbbbbbbbb11111111111" , "log_bbbbbbbbbbbbbbbbbbbb22222222222222222"]
    b_trace_list = ["trbce_bbbbbbbbbbbbbbbbbbbb1111111111111111" , "trbce_bbbbbbbbbbbbbbbbbbbb2222222222222222"]
    b_log_list = json.dumps(b_log_list, ensure_ascii=False).encode('utf-8')
    b_trace_list = json.dumps(b_trace_list, ensure_ascii=False).encode('utf-8')
    r.hset("complete_hash:b456", "parsing_data_log", b_log_list)
    r.hset("complete_hash:b456", "parsing_data_trace", b_trace_list)

    c_log_list = ["log_cccccccccccccccccccc11111111111" , "log_cccccccccccccccccccc22222222222222222"]
    c_trace_list = ["trcce_cccccccccccccccccccc1111111111111111" , "trcce_cccccccccccccccccccc2222222222222222"]
    c_log_list = json.dumps(c_log_list, ensure_ascii=False).encode('utf-8')
    c_trace_list = json.dumps(c_trace_list, ensure_ascii=False).encode('utf-8')
    r.hset("complete_hash:c789", "parsing_data_log", c_log_list)
    r.hset("complete_hash:c789", "parsing_data_trace", c_trace_list)
    d_log_list = ["log_dddddddddddddddddddd11111111111" , "log_dddddddddddddddddddd22222222222222222"]
    d_trace_list = ["trdde_dddddddddddddddddddd1111111111111111" , "trdde_dddddddddddddddddddd2222222222222222"]
    d_log_list = json.dumps(d_log_list, ensure_ascii=False).encode('utf-8')
    d_trace_list = json.dumps(d_trace_list, ensure_ascii=False).encode('utf-8')
    r.hset("complete_hash:d999", "parsing_data_log", d_log_list)
    r.hset("complete_hash:d999", "parsing_data_trace", d_trace_list)

def get_complete_hash():
    key_list = r.keys("complete_hash*")
    return key_list


# test_data_set()
# complete_key_list = get_complete_hash()
# for key in complete_key_list:
#     # hkeys key 이걸로도 모든 키를 조회할수있는데, 일단은 커넥션 안맺고 하는걸로 진행
#     log_data = json.loads(r.hget(key,"parsing_data_log"))
#     trace_data = json.loads(r.hget(key, "parsing_data_trace"))
#     print(log_data)
#     print(trace_data)


def get_complete_parsing_data(r, key):
    hash_key = "complete_hash:" + key
    parsing_log = r.hget(hash_key, "parsing_data_log")
    parsing_trace = r.hget(hash_key, "parsing_data_trace")
    # byte -> str 내용을 가진 list로 변환
    parsing_log = json.loads(parsing_log)
    parsing_trace = json.loads(parsing_trace)
    return parsing_log, parsing_trace


def main():
    while True:
        r = redis.Redis(host='100.83.227.59', port=16379, db=3, password='redis1234!')
        # 테스트 데이터 정의 종료

        # CreateReport 클래스 인스턴스 생성
        report = CreateReport()

        # complete_key_store에서 key 꺼내기
        key = r.lpop("complete_key_store")
        if key is not None:
            key = key.decode('utf-8')
            logging.info(f"* api_batch를 시작합니다. 현재 key는 {key}")

            # complete_hash에서 key에 해당하는 파싱 데이터 꺼내기
            log, trace = get_complete_parsing_data(r, key)

            # DB error_history에 중복이 있는지 체크
            is_duplicate = report.is_duplicate_error(key, trace)
            if is_duplicate is False:
                # 오류리포트 생성 및 저장
                result = report.create_and_save_error_report(key, log, trace)
                if result == "fail":
                    # 메일 발송 실패하면 fail_key_store에 rpush
                    r.rpush("fail_key_store", key)
                    logging.info(f"* fail_key_store에 추가된 키 {key}")

        else:
            logging.info("* complete_key_store에 key가 없습니다.")
            continue

        time.sleep(0.5)