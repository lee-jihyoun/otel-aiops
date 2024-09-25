import redis
import json

# pip install redis
# pip install redis[hiredis]

# Redis 클라이언트 설정
r = redis.Redis(host='100.83.227.59', port=16379, db=1, password='redis1234!')

data_list =({'container.id': 'f2560f55770a7f5076f1dc81341d814b5017820700e56672d9b8a61919b266ad', 'os.description': None, 'process.command_line': None, 'service.name': 'cartservice', 'service.code': 'CA1003', 'telemetry.sdk.language': 'dotnet', 'logRecords_severityText': 'Error', 'logRecords_body_stringValue': "Error when executing service method '{ServiceMethod}'.", 'traceId': 'd08a853b422dd7bfef8a2849cf9d732d', 'observedTimeUnixNano': '2024-09-19 23:40:36'},
            {'container.id': 'f2560f55770a7f5076f1dc81341d814b5017820700e56672d9b8a61919b266ad', 'os.description': None, 'process.command_line': None, 'service.name': 'cartservice', 'service.code': 'CA1003', 'telemetry.sdk.language': 'dotnet', 'logRecords_severityText': 'Error', 'logRecords_body_stringValue': "Error when executing service method '{ServiceMethod}'.", 'traceId': '', 'observedTimeUnixNano': '2024-09-19 23:40:36'},
            {'container.id': '3664da43153e5051d2c104b66787eed90be022efd5f3d45eec9b9a4e47b4c718', 'os.description': 'Linux 5.15.153.1-microsoft-standard-WSL2', 'process.command_line': '/opt/java/openjdk/bin/java -javaagent:/usr/src/app/opentelemetry-javaagent.jar oteldemo.AdService', 'service.name': 'adservice', 'service.code': None, 'telemetry.sdk.language': 'java', 'logRecords_severityText': 'WARN', 'logRecords_body_stringValue': 'GetAds Failed with status Status{code=UNAVAILABLE, description=null, cause=null}', 'traceId': 'ed8b4191838daec751003df550476f1d', 'observedTimeUnixNano': '2024-08-21 22:45:58'},
            {'container.id': '3664da43153e5051d2c104b66787eed90be022efd5f3d45eec9b9a4e47b4c718', 'os.description': 'Linux 5.15.153.1-microsoft-standard-WSL2', 'process.command_line': '/opt/java/openjdk/bin/java -javaagent:/usr/src/app/opentelemetry-javaagent.jar oteldemo.AdService', 'service.name': 'myservice', 'service.code': None, 'telemetry.sdk.language': 'java', 'logRecords_severityText': 'WARN', 'logRecords_body_stringValue': 'GetAds Failed with status Status{code=UNAVAILABLE, description=null, cause=null}', 'traceId': 'ed8b4191838daec751003df550476f1d', 'observedTimeUnixNano': '2024-08-21 22:45:58'})
for i in range(len(data_list)):
    print(i)
    print(data_list[i])

# traceId를 기준으로 데이터를 그룹화하여 Redis에 저장
for log in data_list:
    trace_id = log['traceId']

    # 해시 키는 traceId로 설정
    hash_key = f"filtered_log_hash:{trace_id}"

    # 현재 데이터를 JSON 형식으로 변환
    log_json = json.dumps(log)

    # parsing_data_log 필드가 존재하는지 확인하고, 없으면 리스트로 초기화
    existing_logs = r.hget(hash_key, 'parsing_data_log')
    if existing_logs:
        existing_logs_list = json.loads(existing_logs)
    else:
        existing_logs_list = []

    # 새로운 로그를 리스트에 추가
    existing_logs_list.append(log)
    print("existing_logs")
    print(existing_logs_list)

    # Redis에 업데이트된 리스트 저장 (HSET으로 해시 업데이트)
    r.hset(hash_key, "parsing_data_log", json.dumps(existing_logs_list))

# Redis에 저장된 데이터 확인 (예시)
for log in data_list:
    trace_id = log['traceId']
    hash_key = f"filtered_log_hash:{trace_id}"
    print(f"Redis Key: {hash_key}")
    print(r.hget(hash_key, "parsing_data_log").decode("utf-8"))

# # 저장할 데이터
# data = {
#     "status": "trace",
#     "parsing_data_log": [" 로그 파싱된 데이터"],
#     "parsing_data_trace": [" 트레이스 파싱된 데이터"],
#     "retry": 2,
#     "api": "N"
# }
# json_data = json.dumps(data, ensure_ascii=False).encode('utf-8')
#
# # 데이터를 Redis에 저장 (key: 'trace_key')
# r.set("trace_key", json_data)
#
# # 데이터 조회
# retrieved_data = json.loads(r.get("trace_key"))
# print(retrieved_data)
#
# # 데이터 삭제
# r.delete("trace_key")
#
# # 데이터 조회 - 이미 삭제된 키 가져오려고 해서 오류발생함
# # retrieved_data = json.loads(r.get("trace_key"))
# # print(retrieved_data)
#
# r.set("test","test_data")
#
# # 모든 키 가져오기
# print(r.keys("*"))
#
# print(r.get("test"))
#
# # 모든 키 삭제
# r.flushall()
# # 모든 키 가져오기
# print(r.keys("*"))
#
#
#
# data_01 = {
#     "status": "trace",
#     "parsing_data_log": [" 로그 파싱된 데이터"],
#     "parsing_data_trace": [" 트레이스 파싱된 데이터"],
#     "retry": 2,
#     "api": "N"
# }
# data_02 = {
#     "status": "log",
#     "parsing_data_log": [" 로그 파싱된 데이터"],
#     "parsing_data_trace": [" 트레이스 파싱된 데이터"],
#     "retry": 2,
#     "api": "N"
# }
# data_03 = {
#     "status": "complete",
#     "parsing_data_log": [" 로그 파싱된 데이터"],
#     "parsing_data_trace": [" 트레이스 파싱된 데이터"],
#     "retry": 2,
#     "api": "N"
# }
# # 데이터 저장 및 "complete" 상태인 데이터의 키를 Set에 추가
# r.set('data_01', json.dumps(data_01))
# r.sadd('trace_set', 'data_01')
#
# r.set('data_02', json.dumps(data_02))
# r.sadd('log_set', 'data_02')
#
# r.set('data_03', json.dumps(data_03))
# r.sadd('complete_set', 'data_03')
#
# # "trace" 상태인 데이터 조회
# trace_keys = r.smembers('trace_set')
# trace_data = []
# for key in trace_keys:
#     trace_data.append(json.loads(r.get(key)))
#
# print(trace_data)
# print()
#
# # "log" 상태인 데이터 조회
# log_keys = r.smembers('log_set')
# log_data = []
# for key in log_keys:
#     log_data.append(json.loads(r.get(key)))
#
# print(log_data)
# print()
#
# # "complete" 상태인 데이터 조회
# complete_keys = r.smembers('complete_set')
# complete_data = []
# for key in complete_keys:
#     complete_data.append(json.loads(r.get(key)))
#
# print(complete_data)
# print()
#
# r.flushall()
# r.set("test_data_01" ,"zzzzzzzzzzzzzzzzzzzzzzzzzz")
#
# # 키 만료시간 지정
# r.expire('test_data_01', 10)



'''
### redis-cli 명령어 정리

# 연희가 쓰는 DB 접속하기(0번 DB)
redis-cli -h 127.0.0.1 -p 16379 -n 0

# 해쉬 생성 & 키 최초 삽입
hset key_store:a123 "retry" 0
hset filter_log_hash:a123 "parsing_data_log" "log_parsing_result"
hset filter_trace_hash:a123 "parsing_data_trace" "trace_parsing_result"

hset complete_hash: a123 "parsing_data_log" "log_parsing_result" "parsing_data_trace" "trace_parsing_result"

# 모든 키, 값 조회
hgetall key_store:a123
1) "status"
2) "confirm"
3) "retry"
4) "0"


# 모든 키 삭제
flushall

# 현재 생성되어 있는 모든 키 (데이터가 많은 경우 부하가 심하기 때문에 운영 중인 서비스에선 주의가 필요)
keys *
1) "key_store:a123"

# 특정 키 삭제
del a123

# 특정 키의 값 모두 출력
hvals key_store:a123
1) "confirm"
2) "0"

# 특정 키의 모든 필드 조회
hkeys key_store:a123
1) "status"
2) "retry"


# filter_log_hash에는 키가 있고, filter_trace_hash에는 없는 경우
hset key_store:a123 "retry" 0
hset filter_log_hash:b123 "parsing_data_log" "filter_log_parsing_result"
hset filter_trace_hash:a123 "parsing_data_trace" "filter_trace_parsing_result"

# original 데이터 비교
hset key_store:a123 "retry" 0
hset filter_log_hash:b123 "parsing_data_log" "filter_log_parsing_result"
hset filter_trace_hash:a123 "parsing_data_trace" "filter_trace_parsing_result"
hset original_log_hash:a123 "parsing_data_log" "origin_log_parsing_result"
hset original_trace_hash:b123 "parsing_data_trace" "origin_trace_parsing_result"


1. complete_hash에 잘 들어가는가?
테스트 1. filter_log, filter_trace 존재 (완료)
    hset key_store:a123 "retry" 0
    hset filter_log_hash:a123 "parsing_data_log" "filter_log_parsing_result"
    hset filter_trace_hash:a123 "parsing_data_trace" "filter_trace_parsing_result"
테스트 2. filter_log, original_trace 존재 (완료)
    hset key_store:a123 "retry" 0
    hset filter_log_hash:a123 "parsing_data_log" "filter_log_parsing_result"
    hset original_trace_hash:a123 "parsing_data_trace" "origin_trace_parsing_result"
테스트 3. original_log, filter_trace 존재 (완료)
    hset key_store:a123 "retry" 0
    hset original_log_hash:a123 "parsing_data_log" "origin_log_parsing_result"
    hset filter_trace_hash:a123 "parsing_data_trace" "filter_trace_parsing_result"
테스트 4. original_log, original_trace 존재 -> 안들어가야 함(완료)
    hset key_store:a123 "retry" 0
    hset original_log_hash:a123 "parsing_data_log" "origin_log_parsing_result"
    hset original_trace_hash:b123 "parsing_data_trace" "origin_trace_parsing_result"

2. retry가 잘 되는가?
테스트 1. retry가 2번 이상일때(2~) insert 되는가? (완료)
테스트 2. retry가 1번일때 한번 더 수행되는가? (완료)

3. 조합해보기
테스트 1. origin_trace 빼고 hash가 조회되어야 하며, complete_hash에서 a123은 filter_log, filter_trace를 가져야 함.(완료)
    hset key_store:a123 "retry" 0
    hset filter_log_hash:a123 "parsing_data_log" "filter_log_parsing_result"
    hset filter_trace_hash:a123 "parsing_data_trace" "filter_trace_parsing_result"
    hset original_log_hash:a123 "parsing_data_log" "origin_log_parsing_result"
    hset original_trace_hash:b123 "parsing_data_trace" "origin_trace_parsing_result"

테스트 2. complete_hash에서 a123은 filter_log, filter_trace, b123은 filter_log, origin_trace를 가져야 함. (완료)
    hset key_store:a123 "retry" 0
    hset key_store:b123 "retry" 0
    hset filter_log_hash:a123 "parsing_data_log" "filter_log_parsing_result"
    hset filter_log_hash:b123 "parsing_data_log" "filter_log_parsing_result"
    hset filter_trace_hash:a123 "parsing_data_trace" "filter_trace_parsing_result"
    hset original_log_hash:a123 "parsing_data_log" "origin_log_parsing_result"
    hset original_trace_hash:b123 "parsing_data_trace" "origin_trace_parsing_result"
 

'''