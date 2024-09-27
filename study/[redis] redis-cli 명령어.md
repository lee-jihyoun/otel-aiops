### redis-cli 명령어 정리

# 특정 DB 접속하기(0번 DB)
redis-cli -h 127.0.0.1 -p 16379 -n 0

# 모든 DB의 키 삭제 
flushall

# 특정 DB의 키 삭제
select 0
flushdb

# redis TTL 설정하기(단위는 second)
# 15분
expire key_store:a123 900
# 10분
expire log_hash:a123 600
expire trace_hash:a123 600
# 30분
expire complete_hash:a123 3600

# TTL 확인
ttl complete_hash:a123

# 해쉬 생성 & 키 최초 삽입
hset key_store:a123 "retry" 0
hset filtered_log_hash:a123 "parsing_data_log" "log_parsing_result"
hset filtered_trace_hash:a123 "parsing_data_trace" "trace_parsing_result"
hset complete_hash:a123 "parsing_data_log" "log_parsing_result" "parsing_data_trace" "trace_parsing_result"

hset key_store:b123 "retry" 0
hset filtered_log_hash:b123 "parsing_data_log" "log_parsing_result"
hset filtered_trace_hash:b123 "parsing_data_trace" "trace_parsing_result"

# 진짜 데이터 샘플
hset key_store:d08a853b422dd7bfef8a2849cf9d732d "retry" 0
hset filtered_log_hash:d08a853b422dd7bfef8a2849cf9d732d "parsing_data_log" "[{\"container.id\": \"f2560f55770a7f5076f1dc81341d814b5017820700e56672d9b8a61919b266ad\", \"os.description\": null, \"process.command_line\": null, \"service.name\": \"cartservice\", \"service.code\": \"CA1003\", \"telemetry.sdk.language\": \"dotnet\", \"logRecords_severityText\": \"Error\", \"logRecords_body_stringValue\": \"Error when executing service method '{ServiceMethod}'.\", \"traceId\": \"d08a853b422dd7bfef8a2849cf9d732d\", \"observedTimeUnixNano\": \"2024-09-19 23:40:36\"}, {\"container.id\": \"f2560f55770a7f5076f1dc81341d814b5017820700e56672d9b8a61919b266ad\", \"os.description\": null, \"process.command_line\": null, \"service.name\": \"cartservice\", \"service.code\": \"CA1003\", \"telemetry.sdk.language\": \"dotnet\", \"logRecords_severityText\": \"Error\", \"logRecords_body_stringValue\": \"Error when executing service method '{ServiceMethod}'.\", \"traceId\": \"d08a853b422dd7bfef8a2849cf9d732d\", \"observedTimeUnixNano\": \"2024-09-19 23:40:36\"}, {\"container.id\": \"f2560f55770a7f5076f1dc81341d814b5017820700e56672d9b8a61919b266ad\", \"os.description\": null, \"process.command_line\": null, \"service.name\": \"cartservice\", \"service.code\": \"CA1003\", \"telemetry.sdk.language\": \"dotnet\", \"logRecords_severityText\": \"Error\", \"logRecords_body_stringValue\": \"Error when executing service method '{ServiceMethod}'.\", \"traceId\": \"d08a853b422dd7bfef8a2849cf9d732d\", \"observedTimeUnixNano\": \"2024-09-19 23:40:36\"}, {\"container.id\": \"f2560f55770a7f5076f1dc81341d814b5017820700e56672d9b8a61919b266ad\", \"os.description\": null, \"process.command_line\": null, \"service.name\": \"cartservice\", \"service.code\": \"CA1003\", \"telemetry.sdk.language\": \"dotnet\", \"logRecords_severityText\": \"Error\", \"logRecords_body_stringValue\": \"Error when executing service method '{ServiceMethod}'.\", \"traceId\": \"d08a853b422dd7bfef8a2849cf9d732d\", \"observedTimeUnixNano\": \"2024-09-19 23:40:36\"}]"
hset filtered_trace_hash:d08a853b422dd7bfef8a2849cf9d732d "parsing_data_trace" "[{\"service.name\": \"frontend\", \"service.code\": \"FR1008\", \"os.type\": \"linux\", \"traceId\": \"d08a853b422dd7bfef8a2849cf9d732d\", \"spanId\": \"47e5177b5cfda33b\", \"name\": \"grpc.oteldemo.CartService/GetCart\", \"http.status_code\": null, \"rpc.grpc.status_code\": null, \"exception.message\": null, \"exception.stacktrace\": null, \"exception.stacktrace.short\": null, \"http.url\": null, \"rpc.method\": null, \"startTimeUnixNano\": \"2024-09-19 23:40:31\", \"endTimeUnixNano\": \"2024-09-19 23:40:41\"}, {\"service.name\": \"frontend\", \"service.code\": \"FR1008\", \"os.type\": \"linux\", \"traceId\": \"d08a853b422dd7bfef8a2849cf9d732d\", \"spanId\": \"7c949a6786aa2780\", \"name\": \"executing api route (pages) /api/cart\", \"http.status_code\": \"500\", \"rpc.grpc.status_code\": null, \"exception.message\": \"13 INTERNAL: Received RST_STREAM with code 2 triggered by internal client error: Session closed with error code 2\", \"exception.stacktrace\": \"Error: 13 INTERNAL: Received RST_STREAM with code 2 triggered by internal client error: Session closed with error code 2\\n at callErrorFromStatus (/app/node_modules/@grpc/grpc-js/build/src/call.js:31:19)\\n at Object.onReceiveStatus (/app/node_modules/@grpc/grpc-js/build/src/client.js:193:76)\\n at Object.onReceiveStatus (/app/node_modules/@grpc/grpc-js/build/src/client-interceptors.js:360:141)\\n at Object.onReceiveStatus (/app/node_modules/@grpc/grpc-js/build/src/client-interceptors.js:323:181)\\n at /app/node_modules/@grpc/grpc-js/build/src/resolving-call.js:129:78\\n at process.processTicksAndRejections (node:internal/process/task_queues:77:11)\\nfor call at\\n at ServiceClientImpl.makeUnaryRequest (/app/node_modules/@grpc/grpc-js/build/src/client.js:161:32)\\n at ServiceClientImpl.<anonymous> (/app/node_modules/@grpc/grpc-js/build/src/make-client.js:105:19)\\n at /app/node_modules/@opentelemetry/instrumentation-grpc/build/src/clientUtils.js:131:31\\n at /app/node_modules/@opentelemetry/instrumentation-grpc/build/src/instrumentation.js:211:209\\n at AsyncLocalStorage.run (node:async_hooks:346:14)\\n at AsyncLocalStorageContextManager.with (/app/node_modules/@opentelemetry/context-async-hooks/build/src/AsyncLocalStorageContextManager.js:33:40)\\n at ContextAPI.with (/app/node_modules/@opentelemetry/api/build/src/api/context.js:60:46)\\n at ServiceClientImpl.clientMethodTrace [as getCart] (/app/node_modules/@opentelemetry/instrumentation-grpc/build/src/instrumentation.js:211:42)\\n at /app/.next/server/pages/api/cart.js:1:1025\\n at new ZoneAwarePromise (/app/node_modules/zone.js/bundles/zone.umd.js:1340:33)\", \"exception.stacktrace.short\": \"Error: 13 INTERNAL: Received RST_STREAM with code 2 triggered by internal client error: Session closed with error code 2 at callErrorFromStatus (/app/node_modules/@grpc/grpc-js/build/src/call.js:31:19)\", \"http.url\": null, \"rpc.method\": null, \"startTimeUnixNano\": \"2024-09-19 23:40:31\", \"endTimeUnixNano\": \"2024-09-19 23:40:42\"}, {\"service.name\": \"frontend\", \"service.code\": \"FR1008\", \"os.type\": \"linux\", \"traceId\": \"d08a853b422dd7bfef8a2849cf9d732d\", \"spanId\": \"fa9dabc4b895aae0\", \"name\": \"GET\", \"http.status_code\": null, \"rpc.grpc.status_code\": null, \"exception.message\": null, \"exception.stacktrace\": null, \"exception.stacktrace.short\": null, \"http.url\": null, \"rpc.method\": null, \"startTimeUnixNano\": \"2024-09-19 23:40:31\", \"endTimeUnixNano\": \"2024-09-19 23:40:42\"}]"

# complete_key_store는 list 타입
rpush complete_key_store a123 b123 //오른쪽에서 추가됨
lpop complete_key_store //왼쪽부터 꺼냄

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
