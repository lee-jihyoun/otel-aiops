import time
import logging
import redis
import json

from report_util.create_report import CreateReport


# cd otel_aiops\python-parser
# python -m batch.api_batch

main_dict={}

## 연동 테스트 시 사용
# main_dict = trace_id.main_dict

r = redis.Redis(host='100.83.227.59', port=16379, decode_responses=True, db=5, password='redis1234!')

# 테스트 데이터 삽입
def test_data_set():
    a_log_list = ["log_aaaaaaaaaaaaaaaaaaaa11111111111" , "log_aaaaaaaaaaaaaaaaaaaa22222222222222222"]
    a_trace_list = ["trace_aaaaaaaaaaaaaaaaaaaa1111111111111111" , "trace_aaaaaaaaaaaaaaaaaaaa2222222222222222"]
    a_log_list = json.dumps(a_log_list, ensure_ascii=False).encode('utf-8')
    a_trace_list = json.dumps(a_trace_list, ensure_ascii=False).encode('utf-8')

    r.hset("complete_hash:a123", "parsing_data_log", a_log_list)
    r.hset("complete_hash:a123", "parsing_data_trace", a_trace_list)

    b_log_list = ["log_bbbbbbbbbbbbbbbbbbbb11111111111" , "log_bbbbbbbbbbbbbbbbbbbb22222222222222222"]
    b_trace_list = ["trbce_bbbbbbbbbbbbbbbbbbbb1111111111111111" , "trbce_bbbbbbbbbbbbbbbbbbbb2222222222222222"]
    b_log_list = json.dumps(b_log_list, ensure_ascii=False).encode('utf-8')
    b_trace_list = json.dumps(b_trace_list, ensure_ascii=False).encode('utf-8')
    r.hset("complete_hash:b456", "parsing_data_log", b_log_list)
    r.hset("complete_hash:b456", "parsing_data_trace", b_trace_list)

    c_log_list = ["log_cccccccccccccccccccc11111111111" , "log_cccccccccccccccccccc22222222222222222"]
    c_trace_list = ["trcce_cccccccccccccccccccc1111111111111111" , "trcce_cccccccccccccccccccc2222222222222222"]
    c_log_list = json.dumps(c_log_list, ensure_ascii=False).encode('utf-8')
    c_trace_list = json.dumps(c_trace_list, ensure_ascii=False).encode('utf-8')
    r.hset("complete_hash:c789", "parsing_data_log", c_log_list)
    r.hset("complete_hash:c789", "parsing_data_trace", c_trace_list)
    d_log_list = ["log_dddddddddddddddddddd11111111111" , "log_dddddddddddddddddddd22222222222222222"]
    d_trace_list = ["trdde_dddddddddddddddddddd1111111111111111" , "trdde_dddddddddddddddddddd2222222222222222"]
    d_log_list = json.dumps(d_log_list, ensure_ascii=False).encode('utf-8')
    d_trace_list = json.dumps(d_trace_list, ensure_ascii=False).encode('utf-8')
    r.hset("complete_hash:d999", "parsing_data_log", d_log_list)
    r.hset("complete_hash:d999", "parsing_data_trace", d_trace_list)

def get_complete_hash():
    key_list = r.keys("complete_hash*")
    return key_list


# test_data_set()
# complete_key_list = get_complete_hash()
# for key in complete_key_list:
#     # hkeys key 이걸로도 모든 키를 조회할수있는데, 일단은 커넥션 안맺고 하는걸로 진행
#     log_data = json.loads(r.hget(key,"parsing_data_log"))
#     trace_data = json.loads(r.hget(key, "parsing_data_trace"))
#     print(log_data)
#     print(trace_data)




def main():
    # 테스트 데이터 정의 시작

    # 로그와 스팬 데이터를 정의
    log_data = """
    {
        "container.id": null,
        "os.description": null,
        "process.command_line": null,
        "service.name": "currencyservice",
        "service.code": "CU1005",
        "telemetry.sdk.language": "cpp",
        "logRecords_severityText": "INFO",
        "logRecords_body_stringValue": "Convert conversion successful",
        "traceId": "7097e6b36b89fb6be8fcbbaafffe1302",
        "observedTimeUnixNano": "2024-08-21 23:00:26"
    },
    {
        "container.id": null,
        "os.description": null,
        "process.command_line": null,
        "service.name": "currencyservice",
        "service.code": "CU1005",
        "telemetry.sdk.language": "cpp",
        "logRecords_severityText": "INFO",
        "logRecords_body_stringValue": "Convert conversion successful",
        "traceId": "7097e6b36b89fb6be8fcbbaafffe1302",
        "observedTimeUnixNano": "2024-08-21 23:00:26"
    },
    {
        "container.id": null,
        "os.description": null,
        "process.command_line": null,
        "service.name": "currencyservice",
        "service.code": "CU1005",
        "telemetry.sdk.language": "cpp",
        "logRecords_severityText": "INFO",
        "logRecords_body_stringValue": "Convert conversion successful",
        "traceId": "7097e6b36b89fb6be8fcbbaafffe1302",
        "observedTimeUnixNano": "2024-08-21 23:00:26"
    }
    """
    span_data = """
    {
        "service.name": "checkoutservice",
        "service.code": "CH1004",
        "os.type": "linux",
        "traceId": "7097e6b36b89fb6be8fcbbaafffe1302",
        "spanId": "63227652df31b934",
        "name": "oteldemo.PaymentService/Charge",
        "http.status_code": null,
        "rpc.grpc.status_code": "2",
        "exception.message": null,
        "exception.stacktrace": null,
        "exception.stacktrace.short": null,
        "http.url": null,
        "rpc.method": "Charge",
        "startTimeUnixNano": "2024-08-21 23:00:26",
        "endTimeUnixNano": "2024-08-21 23:00:26"
    },
    {
        "service.name": "checkoutservice",
        "service.code": "CH1004",
        "os.type": "linux",
        "traceId": "7097e6b36b89fb6be8fcbbaafffe1302",
        "spanId": "11549d72d2032a27",
        "name": "oteldemo.CheckoutService/PlaceOrder",
        "http.status_code": null,
        "rpc.grpc.status_code": "13",
        "exception.message": "could not charge the card: rpc error: code = Unknown desc = PaymentService Fail Feature Flag Enabled",
        "exception.stacktrace": null,
        "exception.stacktrace.short": null,
        "http.url": null,
        "rpc.method": "PlaceOrder",
        "startTimeUnixNano": "2024-08-21 23:00:26",
        "endTimeUnixNano": "2024-08-21 23:00:26"
    },
    {
        "service.name": "frontend",
        "service.code": "FR1008",
        "os.type": "linux",
        "traceId": "7097e6b36b89fb6be8fcbbaafffe1302",
        "spanId": "98c7119541a153fb",
        "name": "executing api route (pages) /api/checkout",
        "http.status_code": "500",
        "rpc.grpc.status_code": null,
        "exception.message": "13 INTERNAL: failed to charge card: could not charge the card: rpc error: code = Unknown desc = PaymentService Fail Feature Flag Enabled",
        "exception.stacktrace": "Error: 13 INTERNAL: failed to charge card: could not charge the card: rpc error: code = Unknown desc = PaymentService Fail Feature Flag Enabled\n    at callErrorFromStatus (/app/node_modules/@grpc/grpc-js/build/src/call.js:31:19)\n    at Object.onReceiveStatus (/app/node_modules/@grpc/grpc-js/build/src/client.js:193:76)\n    at Object.onReceiveStatus (/app/node_modules/@grpc/grpc-js/build/src/client-interceptors.js:360:141)\n    at Object.onReceiveStatus (/app/node_modules/@grpc/grpc-js/build/src/client-interceptors.js:323:181)\n    at /app/node_modules/@grpc/grpc-js/build/src/resolving-call.js:129:78\n    at process.processTicksAndRejections (node:internal/process/task_queues:77:11)\nfor call at\n    at ServiceClientImpl.makeUnaryRequest (/app/node_modules/@grpc/grpc-js/build/src/client.js:161:32)\n    at ServiceClientImpl.<anonymous> (/app/node_modules/@grpc/grpc-js/build/src/make-client.js:105:19)\n    at /app/node_modules/@opentelemetry/instrumentation-grpc/build/src/clientUtils.js:131:31\n    at /app/node_modules/@opentelemetry/instrumentation-grpc/build/src/instrumentation.js:211:209\n    at AsyncLocalStorage.run (node:async_hooks:346:14)\n    at AsyncLocalStorageContextManager.with (/app/node_modules/@opentelemetry/context-async-hooks/build/src/AsyncLocalStorageContextManager.js:33:40)\n    at ContextAPI.with (/app/node_modules/@opentelemetry/api/build/src/api/context.js:60:46)\n    at ServiceClientImpl.clientMethodTrace [as placeOrder] (/app/node_modules/@opentelemetry/instrumentation-grpc/build/src/instrumentation.js:211:42)\n    at /app/.next/server/pages/api/checkout.js:1:1041\n    at new ZoneAwarePromise (/app/node_modules/zone.js/bundles/zone.umd.js:1340:33)",
        "exception.stacktrace.short": "Error: 13 INTERNAL: failed to charge card: could not charge the card: rpc error: code = Unknown desc = PaymentService Fail Feature Flag Enabled at callErrorFromStatus (/app/node_modules/@grpc/grpc-js/build/src/call.js:31:19)",
        "http.url": null,
        "rpc.method": null,
        "startTimeUnixNano": "2024-08-21 23:00:26",
        "endTimeUnixNano": "2024-08-21 23:00:26"
    },
    {
        "service.name": "frontend",
        "service.code": "FR1008",
        "os.type": "linux",
        "traceId": "7097e6b36b89fb6be8fcbbaafffe1302",
        "spanId": "be50c0fcc088f2ea",
        "name": "POST",
        "http.status_code": "500",
        "rpc.grpc.status_code": null,
        "exception.message": null,
        "exception.stacktrace": null,
        "exception.stacktrace.short": null,
        "http.url": "http://frontend-proxy:8080/api/checkout",
        "rpc.method": null,
        "startTimeUnixNano": "2024-08-21 23:00:26",
        "endTimeUnixNano": "2024-08-21 23:00:26"
    },
    {
        "service.name": "frontend",
        "service.code": "FR1008",
        "os.type": "linux",
        "traceId": "7097e6b36b89fb6be8fcbbaafffe1302",
        "spanId": "5e3d8f0e54ca4696",
        "name": "grpc.oteldemo.CheckoutService/PlaceOrder",
        "http.status_code": null,
        "rpc.grpc.status_code": "13",
        "exception.message": null,
        "exception.stacktrace": null,
        "exception.stacktrace.short": null,
        "http.url": null,
        "rpc.method": "PlaceOrder",
        "startTimeUnixNano": "2024-08-21 23:00:26",
        "endTimeUnixNano": "2024-08-21 23:00:26"
    },
    {
        "service.name": "loadgenerator",
        "service.code": "LO1009",
        "os.type": null,
        "traceId": "7097e6b36b89fb6be8fcbbaafffe1302",
        "spanId": "ed013ccaa25fdb34",
        "name": "POST",
        "http.status_code": "500",
        "rpc.grpc.status_code": null,
        "exception.message": null,
        "exception.stacktrace": null,
        "exception.stacktrace.short": null,
        "http.url": "http://frontend-proxy:8080/api/checkout",
        "rpc.method": null,
        "startTimeUnixNano": "2024-08-21 23:00:26",
        "endTimeUnixNano": "2024-08-21 23:00:26"
    },
    {
        "service.name": "paymentservice",
        "service.code": "PA1010",
        "os.type": "linux",
        "traceId": "7097e6b36b89fb6be8fcbbaafffe1302",
        "spanId": "e88b55d75ac1a487",
        "name": "grpc.oteldemo.PaymentService/Charge",
        "http.status_code": null,
        "rpc.grpc.status_code": null,
        "exception.message": "PaymentService Fail Feature Flag Enabled",
        "exception.stacktrace": "Error: PaymentService Fail Feature Flag Enabled\n    at module.exports.charge (/usr/src/app/charge.js:21:11)\n    at process.processTicksAndRejections (node:internal/process/task_queues:95:5)\n    at async Object.chargeServiceHandler [as charge] (/usr/src/app/index.js:21:22)",
        "exception.stacktrace.short": "Error: PaymentService Fail Feature Flag Enabled at module.exports.charge (/usr/src/app/charge.js:21:11)",
        "http.url": null,
        "rpc.method": "Charge",
        "startTimeUnixNano": "2024-08-21 23:00:26",
        "endTimeUnixNano": "2024-08-21 23:00:26"
    }
    """

    a123 = {
        "service_code": "PA1010",
        "status": "log",
        "exception_stacktrace": "error_01",
        "exception_stacktrace_short": "short",
        "parsing_data_log": "파싱된 로그 456",
        "parsing_data_trace": "파싱된 트레이스 456",
        "retry": 1,
        "mail": "N"
    }
    b456 = {
        "service_code": "PA1010",
        "status": "trace",
        "exception_stacktrace": "error_02",
        "exception_stacktrace_short": "short",
        "parsing_data_log": "파싱된 로그 789",
        "parsing_data_trace": "파싱된 트레이스 789",
        "retry": 1,
        "mail": "N"
    }
    c789 = {
        "service_code": "PA1010",
        "status": "complete",
        "exception_stacktrace": "error_03",
        "exception_stacktrace_short": "short",
        "parsing_data_log": log_data,
        "parsing_data_trace": span_data,
        "retry": 1,
        "mail": "N"
    }
    # d012={
    #     "service_code" : "PA1010",
    #     "status" : "complete",
    #     "exception_stacktrace" : "error_04",
    #     "parsing_data_log" : "파싱된 로그 123",
    #     "parsing_data_trace" : "파싱된 트레이스 123",
    #     "retry" : 1,
    #     "mail":"N"
    # }

    main_dict = {"a123": a123, "b456": b456, "7097e6b36b89fb6be8fcbbaafffe1302": {
        "service_code": "PA1010",
        "status": "complete",
        "exception_stacktrace": "error_03",
        "exception_stacktrace_short": "exception stacktrace short",
        "parsing_data_log": log_data,
        "parsing_data_trace": span_data,
        "retry": 1,
        "mail": "N"
    }}


    while True:
        # 테스트 데이터 정의 종료

        # CreateReport 클래스 인스턴스 생성
        report_creator = CreateReport()

        # 완료 목록 추출
        complete_dict = report_creator.findCompleteData(main_dict)
        # logging.info(f"* complete_dict: {complete_dict}")

        # DB에서의 error_history와 완료 목록을 비교하여 오류리포트 발송 대상 선정
        error_report_dict = report_creator.compare_db_dict(complete_dict)
        # logging.info(f"* error_report_dict: {error_report_dict}")

        # 2024.09.17 여기까지 테스트 완료
        # 데이터 파싱부분 해결해야함
        # 오류리포트 생성 및 저장
        report_creator.create_and_save_error_report(error_report_dict)

        # 오류 리포트 생성 호출 및 결과 출력
        # report_creator.create_error_report(log_data, span_data)

        # print(report_creator.create_message(log_data, span_data))

        time.sleep(0.5)