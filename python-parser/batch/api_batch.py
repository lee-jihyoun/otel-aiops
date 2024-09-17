from report_util.create_report import CreateReport

# cd otel_aiops\python-parser
# python -m batch.api_batch

main_dict={}

def main():
    
    # 테스트 데이터 정의 시작
    
    # 로그와 스팬 데이터를 정의
    log_data = """    
    {
        "container.id": null,
        "os.description": null,
        "process.command_line": null,
        "service.name": "currencyservice",
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
        "os.type": "linux",
        "traceId": "7097e6b36b89fb6be8fcbbaafffe1302",
        "spanId": "63227652df31b934",
        "name": "oteldemo.PaymentService/Charge",
        "http.status_code": null,
        "rpc.grpc.status_code": "2",
        "exception.message": null,
        "exception.stacktrace": null,
        "http.url": null,
        "rpc.method": "Charge",
        "startTimeUnixNano": "2024-08-21 23:00:26",
        "endTimeUnixNano": "2024-08-21 23:00:26"
    },
    {
        "service.name": "checkoutservice",
        "os.type": "linux",
        "traceId": "7097e6b36b89fb6be8fcbbaafffe1302",
        "spanId": "11549d72d2032a27",
        "name": "oteldemo.CheckoutService/PlaceOrder",
        "http.status_code": null,
        "rpc.grpc.status_code": "13",
        "exception.message": "could not charge the card: rpc error: code = Unknown desc = PaymentService Fail Feature Flag Enabled",
        "exception.stacktrace": null,
        "http.url": null,
        "rpc.method": "PlaceOrder",
        "startTimeUnixNano": "2024-08-21 23:00:26",
        "endTimeUnixNano": "2024-08-21 23:00:26"
    },
    {
        "service.name": "frontend",
        "os.type": "linux",
        "traceId": "7097e6b36b89fb6be8fcbbaafffe1302",
        "spanId": "98c7119541a153fb",
        "name": "executing api route (pages) /api/checkout",
        "http.status_code": "500",
        "rpc.grpc.status_code": null,
        "exception.message": "13 INTERNAL: failed to charge card: could not charge the card: rpc error: code = Unknown desc = PaymentService Fail Feature Flag Enabled",
        "exception.stacktrace": "Error: 13 INTERNAL: failed to charge card: could not charge the card: rpc error: code = Unknown desc = PaymentService Fail Feature Flag Enabled\n    at callErrorFromStatus (/app/node_modules/@grpc/grpc-js/build/src/call.js:31:19)\n    at Object.onReceiveStatus (/app/node_modules/@grpc/grpc-js/build/src/client.js:193:76)\n    at Object.onReceiveStatus (/app/node_modules/@grpc/grpc-js/build/src/client-interceptors.js:360:141)\n    at Object.onReceiveStatus (/app/node_modules/@grpc/grpc-js/build/src/client-interceptors.js:323:181)\n    at /app/node_modules/@grpc/grpc-js/build/src/resolving-call.js:129:78\n    at process.processTicksAndRejections (node:internal/process/task_queues:77:11)\nfor call at\n    at ServiceClientImpl.makeUnaryRequest (/app/node_modules/@grpc/grpc-js/build/src/client.js:161:32)\n    at ServiceClientImpl.<anonymous> (/app/node_modules/@grpc/grpc-js/build/src/make-client.js:105:19)\n    at /app/node_modules/@opentelemetry/instrumentation-grpc/build/src/clientUtils.js:131:31\n    at /app/node_modules/@opentelemetry/instrumentation-grpc/build/src/instrumentation.js:211:209\n    at AsyncLocalStorage.run (node:async_hooks:346:14)\n    at AsyncLocalStorageContextManager.with (/app/node_modules/@opentelemetry/context-async-hooks/build/src/AsyncLocalStorageContextManager.js:33:40)\n    at ContextAPI.with (/app/node_modules/@opentelemetry/api/build/src/api/context.js:60:46)\n    at ServiceClientImpl.clientMethodTrace [as placeOrder] (/app/node_modules/@opentelemetry/instrumentation-grpc/build/src/instrumentation.js:211:42)\n    at /app/.next/server/pages/api/checkout.js:1:1041\n    at new ZoneAwarePromise (/app/node_modules/zone.js/bundles/zone.umd.js:1340:33)",
        "http.url": null,
        "rpc.method": null,
        "startTimeUnixNano": "2024-08-21 23:00:26",
        "endTimeUnixNano": "2024-08-21 23:00:26"
    },
    {
        "service.name": "frontend",
        "os.type": "linux",
        "traceId": "7097e6b36b89fb6be8fcbbaafffe1302",
        "spanId": "be50c0fcc088f2ea",
        "name": "POST",
        "http.status_code": "500",
        "rpc.grpc.status_code": null,
        "exception.message": null,
        "exception.stacktrace": null,
        "http.url": "http://frontend-proxy:8080/api/checkout",
        "rpc.method": null,
        "startTimeUnixNano": "2024-08-21 23:00:26",
        "endTimeUnixNano": "2024-08-21 23:00:26"
    },
    {
        "service.name": "frontend",
        "os.type": "linux",
        "traceId": "7097e6b36b89fb6be8fcbbaafffe1302",
        "spanId": "5e3d8f0e54ca4696",
        "name": "grpc.oteldemo.CheckoutService/PlaceOrder",
        "http.status_code": null,
        "rpc.grpc.status_code": "13",
        "exception.message": null,
        "exception.stacktrace": null,
        "http.url": null,
        "rpc.method": "PlaceOrder",
        "startTimeUnixNano": "2024-08-21 23:00:26",
        "endTimeUnixNano": "2024-08-21 23:00:26"
    },
    {
        "service.name": "loadgenerator",
        "os.type": null,
        "traceId": "7097e6b36b89fb6be8fcbbaafffe1302",
        "spanId": "ed013ccaa25fdb34",
        "name": "POST",
        "http.status_code": "500",
        "rpc.grpc.status_code": null,
        "exception.message": null,
        "exception.stacktrace": null,
        "http.url": "http://frontend-proxy:8080/api/checkout",
        "rpc.method": null,
        "startTimeUnixNano": "2024-08-21 23:00:26",
        "endTimeUnixNano": "2024-08-21 23:00:26"
    },
    {
        "service.name": "paymentservice",
        "os.type": "linux",
        "traceId": "7097e6b36b89fb6be8fcbbaafffe1302",
        "spanId": "e88b55d75ac1a487",
        "name": "grpc.oteldemo.PaymentService/Charge",
        "http.status_code": null,
        "rpc.grpc.status_code": null,
        "exception.message": "PaymentService Fail Feature Flag Enabled",
        "exception.stacktrace": "Error: PaymentService Fail Feature Flag Enabled\n    at module.exports.charge (/usr/src/app/charge.js:21:11)\n    at process.processTicksAndRejections (node:internal/process/task_queues:95:5)\n    at async Object.chargeServiceHandler [as charge] (/usr/src/app/index.js:21:22)",
        "http.url": null,
        "rpc.method": "Charge",
        "startTimeUnixNano": "2024-08-21 23:00:26",
        "endTimeUnixNano": "2024-08-21 23:00:26"
    }
    """


    a123={
        "service_code" : "OG077201",
        "status" : "log",
        "exception_stacktrace" : "error_01",
        "parsing_data_log" : "파싱된 로그 456",
        "parsing_data_trace" : "파싱된 트레이스 456",
        "retry" : 1,
        "mail":"N"
    }
    b456={
        "service_code" : "OG077201",
        "status" : "trace",
        "exception_stacktrace" : "error_02",
        "parsing_data_log" : "파싱된 로그 789",
        "parsing_data_trace" : "파싱된 트레이스 789",
        "retry" : 1,
        "mail":"N"
    }
    c789={
        "service_code" : "OG077201",
        "status" : "complete",
        "exception_stacktrace" : "error_03",
        "parsing_data_log" : log_data,
        "parsing_data_trace" : span_data,
        "retry" : 1,
        "mail":"N"
    }
    d012={
        "service_code" : "OG077201",
        "status" : "complete",
        "exception_stacktrace" : "error_04",
        "parsing_data_log" : "파싱된 로그 123",
        "parsing_data_trace" : "파싱된 트레이스 123",
        "retry" : 1,
        "mail":"N"
    }
    main_dict={"a123" : a123 , "b456" : b456 , "c789" : c789 , "d012" : d012 }

    # 테스트 데이터 정의 종료

    # CreateReport 클래스 인스턴스 생성
    report_creator = CreateReport()

    # 완료 목록 추출
    # complete_dict = report_creator.findCompleteData(main_dict)
    # print('\n * complete_dict:', complete_dict)

    # DB에서의 error_history와 완료 목록을 비교하여 오류리포트 발송 대상 선정
    # error_report_dict = report_creator.compare_db_dict(complete_dict)
    # print('\n * error_report_dict:', error_report_dict)
    
    # 2024.09.17 여기까지 테스트 완료
    # 데이터 파싱부분 해결해야함
    # 오류리포트 생성 및 저장
    # report_creator.create_and_save_error_report(error_report_dict)



    # 오류 리포트 생성 호출 및 결과 출력
    # report_creator.create_error_report(log_data, span_data)

    # print(report_creator.create_message(log_data, span_data))


    # API 호출 및 DB insert 연동
    # 1. input 데이터 전처리: 오류 내용(exception.stacktrace)에 {}가 포함된 경우 전처리하여 api 호출(ex: adServiceFailure)
    log_data = report_creator.remove_json_value(log_data)

    # 2. freesia api 호출
    response = report_creator.create_error_report(log_data, span_data)
    print('\n * response data:', response)

    # 3. response 데이터 escape 문자열 처리
    clean_result = report_creator.make_clean_markdown_json(response)
    print('\n * clean_result:', clean_result)

    # 4. DB insert를 위해 response 데이터 파싱
    service_name, db_data = report_creator.make_db_data(clean_result)
    print('\n * db_data:', db_data)

    # 5. response의 service_name을 이용하여 DB에서 sevice_code를 조회함
    service_code = report_creator.find_service_code(service_name)

    # 6. DB insert
    report_creator.save_error_report(db_data, service_code)
    print("============== api result DB insert 완료 ==============")


main()
