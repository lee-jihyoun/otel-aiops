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


def get_list_key(r, list_info):
    key_list = r.keys(list_info)
    print("(key 정보) key_store에 있는 key는", key_list)
    return key_list


def get_only_key(r, key_info):
    key_ = r.keys(key_info)
    # key_store:a123 형태에서 a123만을 가져옴
    key_list = [key.split(":")[1] for key in key_]
    print("(key 정보)", key_info, "에 있는 key는", key_list)
    return key_list

def get_parsing_data(r, key_info, key):
    key_ = key_info + ":" + key

    # # list 형식일 때
    parsing_data_list = r.lrange(key_, 0, -1)
    # parsing_data_list = [item.decode('utf-8') for item in parsing_data_list]
    print("*", key_, "의 파싱 데이터:", parsing_data_list, "\n")
    return parsing_data_list

    # # hash 형식일 때
    # parsing_data = r.hvals(key_)
    # # str을 list로 변환
    # parsing_data_json = json.dumps(parsing_data)
    # # print("*", key_, "의 파싱 데이터:", parsing_data_json, "\n")
    # return parsing_data_json


def is_retry_over_2(r, key):
    print("(조건) retry가 2 이상인가?")
    retry = int(r.hget(key, "retry"))
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
    print("\n(성공) >>>>>>>>>> complete_hash에 추가 <<<<<<<<<<\n", key, ":", complete_hash_dict)


def main():
    r = get_redis_db_connection()
    while True:
        # key 조회
        key_list = get_list_key(r, "key_store*")
        filtered_log_key_list = get_only_key(r, "filtered_log_list*")
        filtered_trace_key_list = get_only_key(r, "filtered_trace_list*")

        for full_key in key_list:
            key = full_key.split(":")[1]
            print("\n-------------- 현재 key(", key, ")가 포함된 hash 정보 --------------")
            filtered_log = get_parsing_data(r, "filtered_log_list", key)
            filtered_trace = get_parsing_data(r, "filtered_trace_list", key)

            # key의 retry 필드 값을 1 증가(retry 초기값은 0)
            r.hincrby(full_key, "retry", 1)

            if key in filtered_log_key_list and key in filtered_trace_key_list:
                print("\n(조건) filtered_log_list, filtered_trace_lst에 모두 key가 있는가?")
                print("(결과) yes\n")
                result = is_retry_over_2(r, full_key)
                if result:
                    add_complete_hash(r, key, filtered_log, filtered_trace)

            elif key not in filtered_log_key_list and key in filtered_trace_key_list:
                print("(조건) filtered_log_list에는 키가 없고, filtered_trace_list에는 키가 있는가?")
                print("(결과) yes\n")
                original_log_key_list = get_only_key(r, "original_log_list*")
                if key in original_log_key_list:
                    print("(조건) original_log_hash에 키가 있는가?")
                    print("(결과) yes\n")
                    result = is_retry_over_2(r, full_key)
                    if result:
                        original_log = get_parsing_data(r, "original_log_list", key)
                        add_complete_hash(r, key, original_log, filtered_trace)
                else:
                    print("(조건) original_log_hash에 키가 있는가?")
                    print("(결과) no\n")
                    continue

            elif key in filtered_log_key_list and key not in filtered_trace_key_list:
                print("(조건) filtered_log_list에는 키가 있고, filtered_trace_list에는 키가 없는가?")
                print("(결과) yes")
                original_trace_key_list = get_only_key(r, "original_trace_list*")
                if key in original_trace_key_list:
                    print("(조건) original_trace_hash에 키가 있는가?")
                    print("(결과) yes\n")
                    result = is_retry_over_2(r, full_key)
                    if result:
                        original_trace = get_parsing_data(r, "original_trace_list", key)
                        add_complete_hash(r, key, filtered_log, original_trace)
                else:
                    print("(조건) original_trace_hash에 키가 있는가?")
                    print("(결과) no\n")
                    continue
            else:
                print("(조건) filtered_log_list에는 키가 있고, filtered_trace_list에는 키가 없는가?")
                print("(결과) no. 해당 키가 original_log, original_trace 결과만 존재하므로 insert하지 않습니다.\n")
                continue

        # time.sleep(180) # 3분
        time.sleep(30) # 30초

# main()