import time

import redis
import json


def db_connection():
    return redis.Redis(host='100.83.227.59', port=16379, decode_responses=True, db=3, password='redis1234!')


def get_hash_key_list(r, hash_info):
    hash_and_key_list = r.keys(hash_info)
    print("(key 정보) key_store에 있는 hash_key는", hash_and_key_list)
    return hash_and_key_list


def get_key_list(r, hash_info):
    hash_ = r.keys(hash_info)
    # key_store:a123 형태에서 a123만을 가져옴
    hash_key_list = [key.split(":")[1] for key in hash_]
    print("(key 정보)", hash_info, "에 있는 key는", hash_key_list)
    return hash_key_list

def get_parsing_data(r, hash_info, key):
    hash_key = hash_info + ":" + key

    # list 형식일 때
    parsing_data_list = r.lrange(hash_key, 0, -1)
    # parsing_data_list = [item.decode('utf-8') for item in parsing_data_list]
    print("*", hash_info, "의 파싱 데이터:", parsing_data_list, "\n")
    return parsing_data_list

    # hash 형식일 때
    # parsing_data = r.hvals(hash_key)
    # # str을 list로 변환
    # parsing_data_json = json.dumps(parsing_data)
    # # print("*", hash_info, "의 파싱 데이터:", parsing_data_json, "\n")
    # return parsing_data_json


def is_retry_over_2(r, hash_key):
    print("(조건) retry가 2 이상인가?")
    retry = int(r.hget(hash_key, "retry"))
    if retry >= 2:
        print("(결과) yes. retry는", retry)
        return True
    else:
        print("(결과) no. retry는", retry, "입니다. 한번 더 처리가 필요합니다.\n")
        r.hincrby(hash_key, "retry", 1)


def add_complete_hash(r, key, log, trace):
    complete_key = "complete_hash:" + key
    print(type(log))
    print(type(trace))
    r.hset(complete_key, mapping={
        "parsing_data_log": json.dumps(log),
        "parsing_data_trace": json.dumps(trace)
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
    r = db_connection()
    while True:
        # key 조회
        key_list = get_hash_key_list(r, "key_store*")

        for hash_key in key_list:
            key = hash_key.split(":")[1]
            print("\n-------------- 현재 key(", key, ")가 포함된 hash 정보 --------------")
            filtered_log = get_parsing_data(r, "filtered_log_list", key)
            filtered_trace = get_parsing_data(r, "filtered_trace_list", key)
            # 둘다 존재
            if len(filtered_log) >=0 and len(filtered_trace) >=0:
                print("\n(조건) filtered_log_hash, filtered_trace_hash에 모두 key가 있는가?")
                print("(결과) yes\n")
                result = is_retry_over_2(r, hash_key)
                if result:
                    add_complete_hash(r, key, filtered_log, filtered_trace)

            elif len(filtered_log) ==0 and len(filtered_trace) >=0:
                print("(조건) filtered_log_hash에는 키가 없고, filtered_trace_hash에는 키가 있는가?")
                print("(결과) yes\n")
                original_log = get_parsing_data(r, "original_log_list", key)
                if len(original_log) >=0 :
                    print("(조건) original_log_hash에 키가 있는가?")
                    print("(결과) yes\n")
                    result = is_retry_over_2(r, hash_key)
                    if result:
                        add_complete_hash(r, key, original_log, filtered_trace)
                else:
                    print("(조건) original_log_hash에 키가 있는가?")
                    print("(결과) no\n")
                    continue

            elif len(filtered_log) >=0 and len(filtered_trace) ==0:
                print("(조건) filtered_log_hash에는 키가 있고, filtered_trace_hash에는 키가 없는가?")
                print("(결과) yes")
                original_trace = get_parsing_data(r, "original_trace_list", key)
                if key in original_trace:
                    print("(조건) original_trace_hash에 키가 있는가?")
                    print("(결과) yes\n")
                    result = is_retry_over_2(r, hash_key)
                    if result:
                        add_complete_hash(r, key, filtered_log, original_trace)
                else:
                    print("(조건) original_trace_hash에 키가 있는가?")
                    print("(결과) no\n")
                    continue
            else:
                print("(조건) filtered_log_hash에는 키가 있고, filtered_trace_hash에는 키가 없는가?")
                print("(결과) no. 해당 키가 original_log, original_trace 결과만 존재하므로 insert하지 않습니다.\n")
                continue

        # time.sleep(180) # 3분
        time.sleep(30) # 30초

# main()