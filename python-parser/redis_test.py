import redis
import json

# pip install redis
# Redis 클라이언트 설정
r = redis.Redis(host='100.83.227.59', port=16379, db=0, password='redis1234!')

# 저장할 데이터
data = {
    "status": "complete",
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

