
## 데이터베이스 변경
- 초기값은 0으로 설정되어 있음
- select 0
- select 1

## 데이터 삽입 (set)
- set c123 '{"status":"complete","parsing_data_log":["log data"],"parsing_data_trace":["trace data"],"retry":2,"api":null}'

## 데이터 조회 (get)
- get c123
- (결과)
"{\"status\":\"complete\",\"parsing_data_log\":[\"log data\"],\"parsing_data_trace\":[\"trace data\"],\"retry\":2,\"api\":null}"

## 해당 db의 키 값 조회
- keys *
```
- 127.0.0.1:16379> keys *
1) "data_01"
2) "c123"
3) "data"
4) "b123"
```


## 데이터 삭제 (del)
- del b123
- (결과)

```
127.0.0.1:16379> del b123
(integer) 1
127.0.0.1:16379> keys *
1) "data_01"
2) "c123"
3) "data"
```

## Redis 연결 설정

```
r = redis.StrictRedis(
    host='localhost',    # Redis 서버의 호스트
    port=16379,           # Redis 서버의 포트
    password='your_password',  # Redis 비밀번호
    db=0                 # 사용할 데이터베이스 번호 (기본값: 0)
)

# 연결 테스트: Redis에서 간단한 명령 실행
try:
    # PING 명령어로 연결 확인
    response = r.ping()
    if response:
        print("Redis에 성공적으로 연결되었습니다!")
except redis.AuthenticationError:
    print("비밀번호 인증에 실패했습니다.")
except Exception as e:
```

## 파이썬에서 조회된 redis의 필드 파싱
- redis에서는 특정 필드를 추출하는 기능이 없으므로 모든 value를 가져와서 파싱해야 함

```
data = r.get('c123') # Redis에서 c123의 데이터 가져오기 
data_dict = json.loads(data) # 데이터를 JSON으로 디코딩
status = data_dict['status'] # status 필드 조회
print(status)
```