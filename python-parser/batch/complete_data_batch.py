import redis
import json


def get_full_key_list(hash_info):
    full_key_list = r.keys(hash_info)
    # byte 타입을 str로 변환
    full_key_list = [key.decode('utf-8') for key in full_key_list]
    print("*key_store에 있는 키 리스트:", full_key_list)
    return full_key_list


def get_key_list(hash_info):
    hash_ = r.keys(hash_info)
    # byte 타입을 str로 변환
    hash_list = [key.decode('utf-8') for key in hash_]
    # key_store:a123 형태에서 a123만을 가져옴
    hash_key_list = [key.split(":")[1] for key in hash_list]
    print(hash_info, "key:", hash_key_list)
    return hash_key_list


def get_parsing_data(hash_info, key):
    full_key = hash_info + ":" + key
    parsing_data = r.hvals(full_key)
    parsing_data_list = [key.decode('utf-8') for key in parsing_data]
    parsing_data_json = json.dumps(parsing_data_list)
    print(hash_info, "- parsing_data:", parsing_data_json)
    return parsing_data_json


def is_retry_over_2(full_key):
    print("[조건] retry가 2 이상인가?")
    retry = r.hget(full_key, "retry")
    retry = int(retry.decode('utf-8'))
    if retry >= 2:
        print("* retry는 2 이상이고 현재 값은:", retry)
        return True
    else:
        print("* retry는:", retry)
        print("* retry가 1입니다. 한번 더 처리가 필요합니다.")


def add_complete_hash(key, log, trace):
    complete_key = "complete_hash:" + key
    r.hset(complete_key, mapping={
        "parsing_data_log": log,
        "parsing_data_trace": trace
    })
    # 결과 확인
    complete_hash = r.hgetall(complete_key)
    complete_hash_dict = {}
    for field, value in complete_hash.items():
        field = field.decode('utf-8')
        value = value.decode('utf-8')
        complete_hash_dict[field] = value
    print("* complete_hash에 추가 ===> ", key, ":", complete_hash_dict)


# # Redis 클라이언트 설정
r = redis.Redis(host='100.83.227.59', port=16379, db=0, password='redis1234!')

# key 조회
key_list = get_full_key_list("*key_store*")
filter_log_key_list = get_key_list("*filter_log_hash*")
filter_trace_key_list = get_key_list("*filter_trace_hash*")
original_log_key_list = get_key_list("*original_log_hash*")
original_trace_key_list = get_key_list("*original_trace_hash*")

for full_key in key_list:
    key = full_key.split(":")[1]
    print("\n***** 현재 key:", key)
    print("* 현재 키를 가진 hash 조회:")
    filter_log = get_parsing_data("filter_log_hash", key)
    filter_trace = get_parsing_data("filter_trace_hash", key)
    original_log = get_parsing_data("original_log_hash", key)
    original_trace = get_parsing_data("original_trace_hash", key)

    # key의 retry 필드 값을 1 증가(최초 시작: 1)
    r.hincrby(full_key, "retry", 1)

    if key in filter_log_key_list and key in filter_trace_key_list:
        print("[조건] filter_log_hash, filter_trace_hash에 모두 key가 있는가?")
        print("[결과] yes")
        result = is_retry_over_2(full_key)
        if result:
            add_complete_hash(key, filter_log, filter_trace)

    elif key not in filter_log_key_list and key in filter_trace_key_list:
        print("[조건] filter_log_hash에는 키가 없고, filter_trace_hash에는 키가 있는가?")
        print("[결과] yes")
        if key in original_log_key_list:
            print("[조건] original_log_hash에 키가 있는가?")
            print("[결과] yes")
            result = is_retry_over_2(full_key)
            if result:
                add_complete_hash(key, original_log, filter_trace)
        else:
            print("[조건] original_log_hash에 키가 있는가?")
            print("[결과] no")
            continue

    elif key in filter_log_key_list and key not in filter_trace_key_list:
        print("[조건] filter_log_hash에는 키가 있고, filter_trace_hash에는 키가 없는가?")
        print("[결과] yes")
        if key in original_trace_key_list:
            print("[조건] original_trace_hash에 키가 있는가?")
            print("[결과] yes")
            result = is_retry_over_2(full_key)
            if result:
                add_complete_hash(key, filter_log, original_trace)

        else:
            print("[조건] original_trace_hash에 키가 있는가?")
            print("[결과] no")
            continue
    else:
        print("[조건] filter_log_hash에는 키가 있고, filter_trace_hash에는 키가 없는가?")
        print("[결과] no. 해당 키가 original_log, original_trace 결과만 존재하므로 insert하지 않습니다.")
        continue