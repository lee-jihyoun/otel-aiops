import redis
import json


def db_connection():
    return redis.Redis(host='100.83.227.59', port=16379, db=2, password='redis1234!')


def get_hash_key_list(r, hash_info):
    hash_and_key_list = r.keys(hash_info)
    # byte 타입을 str로 변환
    hash_and_key_list = [key.decode('utf-8') for key in hash_and_key_list]
    print("(key 정보) key_store에 있는 hash_key는", hash_and_key_list)
    return hash_and_key_list


def get_key_list(r, hash_info):
    hash_ = r.keys(hash_info)
    # byte 타입을 str로 변환
    hash_list = [key.decode('utf-8') for key in hash_]
    # key_store:a123 형태에서 a123만을 가져옴
    hash_key_list = [key.split(":")[1] for key in hash_list]
    print("(key 정보)", hash_info, "에 있는 key는", hash_key_list)
    return hash_key_list


def get_parsing_data(r, hash_info, key):
    hash_key = hash_info + ":" + key
    parsing_data = r.hvals(hash_key)
    # byte 타입을 str로 디코딩
    parsing_data_list = [key.decode('utf-8') for key in parsing_data]
    parsing_data_json = json.dumps(parsing_data_list)
    print("*", hash_info, "의 파싱 데이터:", parsing_data_json, "\n")
    return parsing_data_json


def is_retry_over_2(r, hash_key):
    print("(조건) retry가 2 이상인가?")
    retry = r.hget(hash_key, "retry")
    retry = int(retry.decode('utf-8'))
    if retry >= 2:
        print("(결과) yes. retry는", retry)
        return True
    else:
        print("(결과)] no. retry는", retry, "입니다. 한번 더 처리가 필요합니다.\n")


def add_complete_hash(r, key, log, trace):
    complete_key = "complete_hash:" + key
    r.hset(complete_key, mapping={
        "parsing_data_log": log,
        "parsing_data_trace": trace
    })
    # 결과 확인
    complete_hash = r.hgetall(complete_key)
    complete_hash_dict = {}
    fields_sort = ["parsing_data_log", "parsing_data_trace"]
    for field in fields_sort:
        value = complete_hash.get(field.encode('utf-8'))
        if value:
            complete_hash_dict[field] = value.decode('utf-8')
    print("\n(성공) complete_hash에 추가 ===>\n", key, ":", complete_hash_dict)


def process_complete_hash():
    # Redis 클라이언트 설정
    r = db_connection()
    # key 조회
    key_list = get_hash_key_list(r, "*key_store*")
    filter_log_key_list = get_key_list(r, "*filtered_log_hash*")
    filter_trace_key_list = get_key_list(r, "*filtered_trace_hash*")

    for hash_key in key_list:
        key = hash_key.split(":")[1]
        print("\n-------------- 현재 key(", key, ")가 포함된 hash 정보 --------------")
        filter_log = get_parsing_data(r, "filtered_log_hash", key)
        filter_trace = get_parsing_data(r, "filtered_trace_hash", key)

        # key의 retry 필드 값을 1 증가(최초 시작: 1)
        r.hincrby(hash_key, "retry", 1)

        if key in filter_log_key_list and key in filter_trace_key_list:
            print("\n(조건) filter_log_hash, filter_trace_hash에 모두 key가 있는가?")
            print("(결과) yes\n")
            result = is_retry_over_2(r, hash_key)
            if result:
                add_complete_hash(r, key, filter_log, filter_trace)

        elif key not in filter_log_key_list and key in filter_trace_key_list:
            print("(조건) filter_log_hash에는 키가 없고, filter_trace_hash에는 키가 있는가?")
            print("(결과) yes\n")
            original_log_key_list = get_key_list(r, "*original_log_hash*")
            if key in original_log_key_list:
                print("(조건) original_log_hash에 키가 있는가?")
                print("(결과) yes\n")
                result = is_retry_over_2(r, hash_key)
                if result:
                    original_log = get_parsing_data(r, "original_log_hash", key)
                    add_complete_hash(r, key, original_log, filter_trace)
            else:
                print("(조건) original_log_hash에 키가 있는가?")
                print("(결과) no\n")
                continue

        elif key in filter_log_key_list and key not in filter_trace_key_list:
            print("(조건) filter_log_hash에는 키가 있고, filter_trace_hash에는 키가 없는가?")
            print("(결과) yes")
            original_trace_key_list = get_key_list(r, "*original_trace_hash*")
            if key in original_trace_key_list:
                print("(조건) original_trace_hash에 키가 있는가?")
                print("(결과) yes\n")
                result = is_retry_over_2(r, hash_key)
                if result:
                    original_trace = get_parsing_data(r, "original_trace_hash", key)
                    add_complete_hash(r, key, filter_log, original_trace)

            else:
                print("(조건) original_trace_hash에 키가 있는가?")
                print("(결과) no\n")
                continue
        else:
            print("(조건) filter_log_hash에는 키가 있고, filter_trace_hash에는 키가 없는가?")
            print("(결과) no. 해당 키가 original_log, original_trace 결과만 존재하므로 insert하지 않습니다.\n")
            continue


# TODO: timesleep은 안에서 걸고, main에서는 스레드로 실행