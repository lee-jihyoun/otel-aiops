import redis
import json

# pip install redis
# pip install redis[hiredis]

# Redis 클라이언트 설정
r = redis.Redis(host='100.83.227.59', port=16379, db=0, password='redis1234!')

# 저장할 데이터
data = {
    "status": "trace",
    "parsing_data_log": [" 로그 파싱된 데이터"],
    "parsing_data_trace": [" 트레이스 파싱된 데이터"],
    "retry": 2,
    "api": "N"
}
json_data = json.dumps(data, ensure_ascii=False).encode('utf-8')

# 데이터를 Redis에 저장 (key: 'trace_key')
r.set("trace_key", json_data)

# 데이터 조회
retrieved_data = json.loads(r.get("trace_key"))
print(retrieved_data)

# 데이터 삭제
r.delete("trace_key")

# 데이터 조회 - 이미 삭제된 키 가져오려고 해서 오류발생함
# retrieved_data = json.loads(r.get("trace_key"))
# print(retrieved_data)

r.set("test","test_data")

# 모든 키 가져오기
print(r.keys("*"))

print(r.get("test"))

# 모든 키 삭제
r.flushall()
# 모든 키 가져오기
print(r.keys("*"))



data_01 = {
    "status": "trace",
    "parsing_data_log": [" 로그 파싱된 데이터"],
    "parsing_data_trace": [" 트레이스 파싱된 데이터"],
    "retry": 2,
    "api": "N"
}
data_02 = {
    "status": "log",
    "parsing_data_log": [" 로그 파싱된 데이터"],
    "parsing_data_trace": [" 트레이스 파싱된 데이터"],
    "retry": 2,
    "api": "N"
}
data_03 = {
    "status": "complete",
    "parsing_data_log": [" 로그 파싱된 데이터"],
    "parsing_data_trace": [" 트레이스 파싱된 데이터"],
    "retry": 2,
    "api": "N"
}
# 데이터 저장 및 "complete" 상태인 데이터의 키를 Set에 추가
r.set('data_01', json.dumps(data_01))
r.sadd('trace_set', 'data_01')

r.set('data_02', json.dumps(data_02))
r.sadd('log_set', 'data_02')

r.set('data_03', json.dumps(data_03))
r.sadd('complete_set', 'data_03')

# "trace" 상태인 데이터 조회
trace_keys = r.smembers('trace_set')
trace_data = []
for key in trace_keys:
    trace_data.append(json.loads(r.get(key)))

print(trace_data)
print()

# "log" 상태인 데이터 조회
log_keys = r.smembers('log_set')
log_data = []
for key in log_keys:
    log_data.append(json.loads(r.get(key)))

print(log_data)
print()

# "complete" 상태인 데이터 조회
complete_keys = r.smembers('complete_set')
complete_data = []
for key in complete_keys:
    complete_data.append(json.loads(r.get(key)))

print(complete_data)
print()

r.flushall()
r.set("test_data_01" ,"zzzzzzzzzzzzzzzzzzzzzzzzzz")

# 키 만료시간 지정
r.expire('test_data_01', 10)

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

'''