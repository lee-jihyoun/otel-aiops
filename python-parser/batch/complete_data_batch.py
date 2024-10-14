import time
import json
import configparser
import redis


def get_redis_db_connection():
    config = configparser.ConfigParser()
    config.read('./config/db_config.ini')
    host = config['redis-DB']['DB_HOST']
    port = config['redis-DB']['DB_PORT']
    pwd = config['redis-DB']['DB_PWD']
    db_num = config['redis-DB']['DB']
    conn = redis.Redis(host=host, port=port, decode_responses=True, db=db_num, password=pwd)
    return conn


def get_parsing_data(r, key_info, key):
    key_ = key_info + ":" + key
    # # list 형식일 때
    parsing_data_list = r.lrange(key_, 0, -1)
    # print("*", key_, "의 파싱 데이터:", parsing_data_list, "\n")
    return parsing_data_list

    # # hash 형식일 때
    # parsing_data = r.hvals(key_)
    # # str을 list로 변환
    # parsing_data_json = json.dumps(parsing_data)
    # # # print("*", key_, "의 파싱 데이터:", parsing_data_json, "\n")
    # return parsing_data_json


def create_retry_count_store(r, retry_count_store):
    r.hset(retry_count_store, "retry", "0")
    r.expire(retry_count_store, 60*15)


def is_retry_over_2(r, key):
    # print("(조건) retry가 2 이상인가?")
    retry_count_store = "retry_count_store:" + key
    # retry_count_store에 해당 키가 없으면 새로 생성
    if not r.exists(retry_count_store):
        create_retry_count_store(r, retry_count_store)

    # retry_count_store에 저장된 key의 retry 필드 값을 1 증가(retry 초기값은 0)
    r.hincrby(retry_count_store, "retry", 1)
    retry = int(r.hget(retry_count_store, "retry"))
    if retry >= 2:
        print("(결과) yes. retry는", retry)
        return True
    else:
        print("(결과) no. retry는", retry, "입니다. 한번 더 처리가 필요합니다.\n")


def add_complete_hash(r, key, log, trace):
    complete_key = "complete_hash:" + key
    # hset 명령어는 문자열만 허용하므로 list 타입을 문자열로 변환
    log = json.dumps(log)
    trace = json.dumps(trace)
    r.hset(complete_key, mapping={
        "parsing_data_log": log,
        "parsing_data_trace": trace
    })
    # complete_hash expire 설정(15분)
    r.expire(complete_key, 900)
    # complete_key_store(list 타입)에도 넣어줌
    r.rpush("complete_key_store", key)
    # 결과 확인
    complete_hash = r.hgetall(complete_key)
    complete_hash_dict = {}
    fields_sort = ["parsing_data_log", "parsing_data_trace"]
    for field in fields_sort:
        value = complete_hash.get(field)
        if value:
            complete_hash_dict[field] = value
    # print("\n(성공) >>>>>>>>>> complete_hash에 추가 <<<<<<<<<<\n", key, ":", complete_hash_dict)


def main():
    r = get_redis_db_connection()
    while True:
        # print("************* complete_data_batch start *************")
        key_store_set = r.smembers("key_store")
        # # print(type(set_values))
        # key_store_list = r.lrange("key_store", 0, -1)
        # # print("key_store_list:", key_store_list)
        # key_store 리스트에서 key 꺼내기
        for key in key_store_set:
            # print("\n-------------- 현재 key(", key, ")가 포함된 hash 정보 --------------")
            filtered_log = get_parsing_data(r, "filtered_log_list", key)
            filtered_trace = get_parsing_data(r, "filtered_trace_list", key)

            # filtered_log, filtered_trace 둘다 존재
            if len(filtered_log) > 0 and len(filtered_trace) > 0:
                # print("\n(조건) filtered_log_list, filtered_trace_lst에 모두 key가 있는가?")
                # print("(결과) yes\n")
                result = is_retry_over_2(r, key)
                if result:
                    add_complete_hash(r, key, filtered_log, filtered_trace)

            elif len(filtered_log) == 0 and len(filtered_trace) > 0:
                # print("(조건) filtered_log_list에는 키가 없고, filtered_trace_list에는 키가 있는가?")
                # print("(결과) yes\n")
                original_log = get_parsing_data(r, "original_log_list", key)
                if len(original_log) > 0:
                    # print("(조건) original_log_hash에 키가 있는가?")
                    # print("(결과) yes\n")
                    result = is_retry_over_2(r, key)
                    if result:
                        add_complete_hash(r, key, original_log, filtered_trace)
                else:
                    # print("(조건) original_log_hash에 키가 있는가?")
                    # print("(결과) no\n")
                    continue

            elif len(filtered_log) > 0 and len(filtered_trace) == 0:
                # print("(조건) filtered_log_list에는 키가 있고, filtered_trace_list에는 키가 없는가?")
                # print("(결과) yes")
                original_trace = get_parsing_data(r, "original_trace_list", key)
                if len(original_trace) > 0:
                    # print("(조건) original_trace_hash에 키가 있는가?")
                    # print("(결과) yes\n")
                    result = is_retry_over_2(r, key)
                    if result:
                        add_complete_hash(r, key, filtered_log, original_trace)
                else:
                    # print("(조건) original_trace_hash에 키가 있는가?")
                    # print("(결과) no\n")
                    continue
            else:
                # print("(조건) filtered_log_list에는 키가 있고, filtered_trace_list에는 키가 없는가?")
                # print("(결과) no. 해당 키가 original_log, original_trace 결과만 존재하므로 insert하지 않습니다.\n")
                continue

        # time.sleep(180) # 3분
        time.sleep(30) # 30초

# main()