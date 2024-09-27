import time, json
import logging
import datetime

# 초기 인덱스 설정
last_position = 0

error_message = '''Error: 13 INTERNAL: Received RST_STREAM with code 2 triggered by internal client error: Session closed with error code 2\n at callErrorFromStatus (/app/node_modules/@grpc/grpc-js/build/src/call.js:31:19)\n at Object.onReceiveStatus (/app/node_modules/@grpc/grpc-js/build/src/client.js:193:76)\n at Object.onReceiveStatus (/app/node_modules/@grpc/grpc-js/build/src/client-interceptors.js:360:141)\n at Object.onReceiveStatus (/app/node_modules/@grpc/grpc-js/build/src/client-interceptors.js:323:181)\n at /app/node_modules/@grpc/grpc-js/build/src/resolving-call.js:129:78\n at process.processTicksAndRejections (node:internal/process/task_queues:77:11)\nfor call at\n at ServiceClientImpl.makeUnaryRequest (/app/node_modules/@grpc/grpc-js/build/src/client.js:161:32)\n at ServiceClientImpl.<anonymous> (/app/node_modules/@grpc/grpc-js/build/src/make-client.js:105:19)\n at /app/node_modules/@opentelemetry/instrumentation-grpc/build/src/clientUtils.js:131:31)\n at /app/node_modules/@opentelemetry/instrumentation-grpc/build/src/instrumentation.js:211:209)\n at AsyncLocalStorage.run (node:async_hooks:346:14)\n at AsyncLocalStorageContextManager.with (/app/node_modules/@opentelemetry/context-async-hooks/build/src/AsyncLocalStorageContextManager.js:33:40)\n at ContextAPI.with (/app/node_modules/@opentelemetry/api/build/src/api/context.js:60:46)\n at ServiceClientImpl.clientMethodTrace [as getCart] (/app/node_modules/@opentelemetry/instrumentation-grpc/build/src/instrumentation.js:211:42)\n at /app/.next/server/pages/api/cart.js:1:1025'''
# error_message = '''null'''
# Split the string by newlines and get the first two lines
first_two_lines = '\n'.join(error_message.split('\n')[:3])
new = error_message.split('\n')[:2]
print(' '.join(line.strip() for line in new))
print(first_two_lines)

# # 파일을 주기적으로 읽는 함수
# def monitor_file(input_path, file_name):
#     global last_position
#
#     with open(input_path + file_name, "r", encoding='utf-8') as log_file:
#         # 파일 포인터를 마지막 읽은 위치로 이동
#         log_file.seek(last_position)
#
#         while True:
#             # 새로운 로그 읽기
#             # for line in log_file:
#             #     print(line)
#             line = log_file.readline()  # 한 줄씩 읽기
#
#             if not line:  # 더 이상 읽을 데이터가 없으면
#                 break  # 루프를 종료
#
#             # 디버깅할 때 사용..
#             print(f"* 새로 읽은 데이터: {line.strip()}")
#             print(json.loads(line.strip()))
#             logging.info(f"================ filtered_log 파싱 start: {datetime.datetime.now()} ================")
#
#         # 마지막으로 읽은 위치를 업데이트
#         last_position = log_file.tell()  # 현재 파일 포인터의 위치를 저장
#         print(last_position)
#
#
# # 주기적으로 파일을 모니터링
# while True:
#     print("-=-=-=-=-----------파일 읽기 시작-=-=----------")
#     monitor_file("", "filtered_logs.json")
#     time.sleep(5)  # 5초마다 새 로그 확인