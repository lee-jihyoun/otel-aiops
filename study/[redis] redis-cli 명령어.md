### redis-cli 명령어 정리

# 특정 DB 접속하기(0번 DB)
redis-cli -h 127.0.0.1 -p 16379 -n 0

# redis TTL 설정하기(단위는 second)
# 15분
expire key_store:a123 900
# 10분
expire log_hash:a123 600
expire trace_hash:a123 600
# 30분
expire complete_hash:a123 3600

# 해쉬 생성 & 키 최초 삽입
hset key_store:a123 "retry" 0
hset filtered_log_hash:a123 "parsing_data_log" "log_parsing_result"
hset filtered_trace_hash:a123 "parsing_data_trace" "trace_parsing_result"
hset complete_hash: a123 "parsing_data_log" "log_parsing_result" "parsing_data_trace" "trace_parsing_result"
hset complete_key_store: a123 "status" "complete"
set complete_key_store a123

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


# filtered_log_hash에는 키가 있고, filtered_trace_hash에는 없는 경우
hset key_store:a123 "retry" 0
hset filtered_log_hash:b123 "parsing_data_log" "filtered_log_parsing_result"
hset filtered_trace_hash:a123 "parsing_data_trace" "filtered_trace_parsing_result"

# original 데이터 비교
hset key_store:a123 "retry" 0
hset filtered_log_hash:b123 "parsing_data_log" "filtered_log_parsing_result"
hset filtered_trace_hash:a123 "parsing_data_trace" "filtered_trace_parsing_result"
hset original_log_hash:a123 "parsing_data_log" "origin_log_parsing_result"
hset original_trace_hash:b123 "parsing_data_trace" "origin_trace_parsing_result"

### 테스트 
1. complete_hash에 잘 들어가는가?
테스트 1. filtered_log, filtered_trace 존재 (완료)
   hset key_store:a123 "retry" 0
   hset filtered_log_hash:a123 "parsing_data_log" "filtered_log_parsing_result"
   hset filtered_trace_hash:a123 "parsing_data_trace" "filtered_trace_parsing_result"
테스트 2. filtered_log, original_trace 존재 (완료)
   hset key_store:a123 "retry" 0
   hset filtered_log_hash:a123 "parsing_data_log" "filtered_log_parsing_result"
   hset original_trace_hash:a123 "parsing_data_trace" "origin_trace_parsing_result"
테스트 3. original_log, filtered_trace 존재 (완료)
   hset key_store:a123 "retry" 0
   hset original_log_hash:a123 "parsing_data_log" "origin_log_parsing_result"
   hset filtered_trace_hash:a123 "parsing_data_trace" "filtered_trace_parsing_result"
테스트 4. original_log, original_trace 존재 -> 안들어가야 함(완료)
   hset key_store:a123 "retry" 0
   hset original_log_hash:a123 "parsing_data_log" "origin_log_parsing_result"
   hset original_trace_hash:b123 "parsing_data_trace" "origin_trace_parsing_result"

2. retry가 잘 되는가?
테스트 1. retry가 2번 이상일때(2~) insert 되는가? (완료)
테스트 2. retry가 1번일때 한번 더 수행되는가? (완료)

3. 조합해보기
테스트 1. origin_trace 빼고 hash가 조회되어야 하며, complete_hash에서 a123은 filtered_log, filtered_trace를 가져야 함.(완료)
   hset key_store:a123 "retry" 0
   hset filtered_log_hash:a123 "parsing_data_log" "filtered_log_parsing_result"
   hset filtered_trace_hash:a123 "parsing_data_trace" "filtered_trace_parsing_result"
   hset original_log_hash:a123 "parsing_data_log" "origin_log_parsing_result"
   hset original_trace_hash:b123 "parsing_data_trace" "origin_trace_parsing_result"

테스트 2. complete_hash에서 a123은 filtered_log, filtered_trace, b123은 filtered_log, origin_trace를 가져야 함. (완료)
    hset key_store:a123 "retry" 0
    hset key_store:b123 "retry" 0
    hset filtered_log_hash:a123 "parsing_data_log" "filtered_log_parsing_result"
    hset filtered_log_hash:b123 "parsing_data_log" "filtered_log_parsing_result"
    hset filtered_trace_hash:a123 "parsing_data_trace" "filtered_trace_parsing_result"
    hset original_log_hash:a123 "parsing_data_log" "origin_log_parsing_result"
    hset original_trace_hash:b123 "parsing_data_trace" "origin_trace_parsing_result"
