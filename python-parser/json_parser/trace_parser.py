import json, itertools, datetime
from util.datetime_util import change_timenano_format
import variables.trace_id as trace_id
import variables.file_idx as file_idx


class TraceParsing:

    def __init__(self, input_path, filtered_file_name, original_file_name, filtered_idx, original_idx):
        self.input_path = input_path
        self.filtered_file_name = filtered_file_name
        self.original_file_name = original_file_name
        self.filtered_idx = filtered_idx
        self.original_idx = original_idx

    def process_filtered_trace(self, main_dict, span, parsed_trace):
        # 상태가 log인가?
        print("상태가 log인가?\n")
        trace_status_entries = {key: value for key, value in main_dict.items() if
                                isinstance(value, dict) and value.get('status') == 'log'}
        print('* trace_status_entries:', trace_status_entries)

        # main_dict에 상태값이 log인가 (trace_status_entries 내에 main_dict가 존재하는가) (Y)
        if len(trace_status_entries) > 0:
            print("main_dict에 상태값이 log인가 (trace_status_entries 내에 main_dict가 존재하는가) (Y)\n")

            # 파싱된 로그와 딕셔너리에 있는 trace ID값이 일치 하는가 (Y)
            if span["traceId"] in trace_status_entries:
                print("파싱된 트레이스와 딕셔너리에 있는 trace ID값이 일치 하는가 (Y)\n")
                matching_trace = [data for data in parsed_trace if data.get("traceId") == span["traceId"]]
                if matching_trace:
                    main_dict[span["traceId"]]["status"] = "confirm"
                    main_dict[span["traceId"]]["parsing_data_trace"] = matching_trace
                    print('* main_dict:', main_dict)

            else:
                print("파싱된 트레이스와 딕셔너리에 있는 trace ID값이 일치 하는가 (N)\n")
                self.original_trace_parser()
                # pass

            # 파싱된 트레이스에 trace ID가 있는가? (Y)
            if "traceId" in span and span["traceId"] != "":
                print("파싱된 트레이스에 trace ID가 있는가? (Y)\n")

                # main_dict에 key가 있는가? (N)
                if span["traceId"] not in main_dict:
                    print("main_dict에 key가 있는가? (N)\n")
                    print("parsed_trace*******")
                    print(parsed_trace)
                    for co_parsed_trace in parsed_trace:
                        co_parsed_trace["traceId"] = span["traceId"]
                        main_dict[span["traceId"]] = {"status": "trace",
                                                      "parsing_data_log": "",
                                                      "parsing_data_trace": parsed_trace,
                                                      "retry": 0,
                                                      "mail": "N"}

                    print('* main_dict:', main_dict)

                # main_dict에 key가 있는가? (Y)
                else:
                    print("# main_dict에 key가 있는가? (Y)\n")
                    print('* main_dict:', main_dict)
                    matching_trace = [data for data in parsed_trace if data.get("traceId") == span["traceId"]]
                    if matching_trace:
                        main_dict[span["traceId"]]["status"] = "confirm"
                        main_dict[span["traceId"]]["parsing_data_trace"] = matching_trace
                        print('* main_dict:', main_dict)

            # 파싱된 로그에 trace ID가 있는가? (N)
            else:
                print("# 파싱된 로그에 trace ID가 있는가? (N)\n")
                pass

        # main_dict에 상태값이 log인가 (trace_status_entries 내에 main_dict가 존재하는가) (Y)
        elif len(trace_status_entries) > 0 and span["traceId"] in trace_status_entries:
            print("main_dict에 상태값이 log인가 (trace_status_entries 내에 main_dict가 존재하는가) (Y)\n")

            # 파싱된 로그와 딕셔너리에 있는 trace ID값이 일치 하는가 (Y)
            if span["traceId"] in trace_status_entries:
                print("파싱된 트레이스와 딕셔너리에 있는 trace ID값이 일치 하는가 (Y)\n")
                matching_trace = [data for data in parsed_trace if data.get("traceId") == span["traceId"]]
                if matching_trace:
                    main_dict[span["traceId"]]["status"] = "confirm"
                    main_dict[span["traceId"]]["parsing_data_trace"] = matching_trace
                    print('* main_dict:', main_dict)

            else:
                print("파싱된 트레이스와 딕셔너리에 있는 trace ID값이 일치 하는가 (N)\n")
                self.original_trace_parser()
                # pass

        else:
            print("main_dict에 상태값이 log인가 (N)\n")

            # 파싱된 트레이스에 trace ID가 있는가? (Y)
            if "traceId" in span and span["traceId"] != "":
                print("파싱된 트레이스에 trace ID가 있는가? (Y)\n")

                # main_dict에 key가 있는가? (N)
                if span["traceId"] not in main_dict:
                    print("main_dict에 key가 있는가? (N)\n")
                    for co_parsed_trace in parsed_trace:
                        co_parsed_trace["traceId"] = span["traceId"]
                        main_dict[span["traceId"]] = {"status": "trace",
                                                      "parsing_data_log": "",
                                                      "parsing_data_trace": parsed_trace,
                                                      "retry": 0,
                                                      "mail": "N"}

                        print('* main_dict:', main_dict)

                # main_dict에 key가 있는가? (Y)
                else:
                    print("# main_dict에 key가 있는가? (Y)\n")
                    matching_trace = [data for data in parsed_trace if data.get("traceId") == span["traceId"]]
                    if matching_trace:
                        main_dict[span["traceId"]]["status"] = "confirm"
                        main_dict[span["traceId"]]["parsing_data_trace"] = matching_trace
                        print('* main_dict:', main_dict)

            # 파싱된 로그에 trace ID가 있는가? (N)
            else:
                print("# 파싱된 스팬에 trace ID가 있는가? (N)\n")
                pass

    def process_original_trace(self, main_dict, span, parsed_trace):
        # 상태가 log인가?
        print("상태가 log인가?\n")
        trace_status_entries = {key: value for key, value in main_dict.items() if
                                isinstance(value, dict) and value.get('status') == 'log'}
        print(trace_status_entries)

        # main_dict에 상태값이 log인가 (trace_status_entries 내에 main_dict가 존재하는가) (Y)
        if len(trace_status_entries) > 0:
            print("main_dict에 상태값이 log인가 (trace_status_entries 내에 main_dict가 존재하는가) (Y)\n")

            # 원문로그에 해당 trace id 가 있는가 (Y)
            if span["traceId"] in trace_status_entries:
                print("원문로그에 해당 trace id 가 있는가 (Y)\n")
                matching_trace = [data for data in parsed_trace if data.get("traceId") == span["traceId"]]
                if matching_trace:
                    main_dict[span["traceId"]]["status"] = "confirm"
                    main_dict[span["traceId"]]["parsing_data_trace"] = matching_trace

            else:
                # main_dict에 있는 해당 키의 리트라이 횟수가 3 미만인가
                print("main_dict에 있는 해당 키의 리트라이 횟수가 3 미만인가 (Y)\n")
                # trace_status_entries에서 retry 값을 1씩 증가
                for trace_id, trace_info in trace_status_entries.items():
                    if trace_info.get("retry", 0) < 3:  # retry가 3 미만일 때만 증가
                        trace_info["retry"] += 1
                        print(f"Trace ID: {trace_id}, Retry 증가: {trace_info['retry']}")
                        # break
                    else:
                        trace_info["status"] = 'confirm'
                        print(f"Trace ID: {trace_id}, Retry 횟수가 이미 3에 도달")

    def filtered_trace_parser(self):
        input_path = self.input_path
        file_name = self.filtered_file_name
        idx = self.filtered_idx

        parsing_trace_data_list = [] # "a111", "b111"
        with open(input_path + file_name, "r") as span_file:
            for current_index, line in enumerate(itertools.islice(span_file, idx, None), start=idx):
                main_dict = trace_id.main_dict
                print("================ filtered_span 파싱 start :", datetime.datetime.now(), "================")
                # 디버깅할 때 사용..
                print('* 아무 글자나 입력:')
                input()

                try:
                    span_data = json.loads(line.strip())
                    change_timenano_format(span_data)
                    print('* span_data:', span_data)

                    for resource in span_data.get('resourceSpans', []):
                        service_name = None
                        os_type = None

                        # if "resource" in resource_log and "attributes" in resource_log["resource"]:
                        if "resource" in resource and "attributes" in resource["resource"]:
                            for attribute in resource["resource"]["attributes"]:
                                if attribute["key"] == "service.name":
                                    service_name = attribute["value"]["stringValue"]
                                if attribute["key"] == "service.code":
                                    service_code = attribute["value"]["stringValue"]
                                else:
                                    service_code = None
                                if attribute["key"] == "os.type":
                                    os_type = attribute["value"]["stringValue"]

                        # log_parser에서 for scope_log in resource_log.get("scopeLogs", []):
                        for scopeSpan in resource.get("scopeSpans", []):
                            for span in scopeSpan.get("spans", []):

                                parsed_info = {
                                    "service.name": service_name,
                                    "service.code": service_code,
                                    "os.type": os_type,
                                    "traceId": span.get("traceId"),
                                    "spanId": span.get("spanId"),
                                    "name": span.get("name"),
                                    "http.status_code": None,
                                    "rpc.grpc.status_code": None,
                                    "exception.message": None,
                                    "exception.stacktrace": None,
                                    "http.url": None,
                                    "rpc.method": None,
                                    "startTimeUnixNano": span.get("startTimeUnixNano"),
                                    "endTimeUnixNano": span.get("endTimeUnixNano")
                                }

                                # trace에서는 scopespan 안에 attribute가 따로 있음
                                for attribute in span.get("attributes", []):
                                    try:
                                        if attribute["key"] == "http.status_code":
                                            parsed_info["http.status_code"] = attribute["value"]["intValue"]
                                        if attribute["key"] == "rpc.grpc.status_code":
                                            parsed_info["rpc.grpc.status_code"] = attribute["value"]["intValue"]
                                        if attribute["key"] == "http.url":
                                            parsed_info["http.url"] = attribute["value"]["stringValue"]
                                        if attribute["key"] == "rpc.method":
                                            parsed_info["rpc.method"] = attribute["value"]["stringValue"]
                                    except KeyError as e:
                                        print(f"Key is not found: {e}")
                                        continue
                                # event 발생 시 event key 내에 exception.message와 exception.stacktrace가 따로 있음
                                for event in span.get("events", []):
                                    for attribute in event.get("attributes", []):
                                        if attribute["key"] == "exception.message":
                                            parsed_info["exception.message"] = attribute["value"]["stringValue"]
                                        if attribute["key"] == "exception.stacktrace":
                                            parsed_info["exception.stacktrace"] = attribute["value"]["stringValue"]

                                # span이 여러개인 경우 list에 파싱 결과를 append하여 전달
                                parsing_trace_data_list.append(parsed_info)

                except json.JSONDecodeError as e:
                    print(f"Error parsing line: {e}")
                # print("* parsing_trace_data_list:", parsing_trace_data_list)

                self.process_filtered_trace(main_dict, span, parsing_trace_data_list)
                print("================ filtered_span 파싱 end ================\n")
                print("* filtered_idx:", current_index)
                file_idx.idx["filtered_span"] = current_index + 1
                print("* filter_span_parsed_end_dictionary:", trace_id.main_dict)

    def original_trace_parser(self):

        input_path = self.input_path
        file_name = self.original_file_name
        idx = self.original_idx

        parsing_trace_data_list = []

        with open(input_path + file_name, "r") as span_file:
            for current_index, line in enumerate(itertools.islice(span_file, idx, None), start=idx):
                main_dict = trace_id.main_dict
                print("================ original_span 파싱 start :", datetime.datetime.now(), "================")

                # 디버깅할 때 사용..
                print('* 아무 글자나 입력:')
                input()

                try:
                    span_data = json.loads(line.strip())
                    change_timenano_format(span_data)
                    print('* span_data:', span_data)

                    for resource in span_data.get('resourceSpans', []):
                        service_name = None
                        os_type = None

                        # if "resource" in resource_log and "attributes" in resource_log["resource"]:
                        if "resource" in resource and "attributes" in resource["resource"]:
                            for attribute in resource["resource"]["attributes"]:
                                if attribute["key"] == "service.name":
                                    service_name = attribute["value"]["stringValue"]
                                if attribute["key"] == "service.code":
                                    service_code = attribute["value"]["stringValue"]
                                else:
                                    service_code = None
                                if attribute["key"] == "os.type":
                                    os_type = attribute["value"]["stringValue"]

                                    # log_parser에서 for scope_log in resource_log.get("scopeLogs", []):
                        for scopeSpan in resource.get("scopeSpans", []):
                            for span in scopeSpan.get("spans", []):

                                parsed_info = {
                                    "service.name": service_name,
                                    "service.code": service_code,
                                    "os.type": os_type,
                                    "traceId": span.get("traceId"),
                                    "spanId": span.get("spanId"),
                                    "name": span.get("name"),
                                    "http.status_code": None,
                                    "rpc.grpc.status_code": None,
                                    "exception.message": None,
                                    "exception.stacktrace": None,
                                    "http.url": None,
                                    "rpc.method": None,
                                    "startTimeUnixNano": span.get("startTimeUnixNano"),
                                    "endTimeUnixNano": span.get("endTimeUnixNano")
                                }

                                # trace에서는 scopespan 안에 attribute가 따로 있음
                                for attribute in span.get("attributes", []):
                                    try:
                                        if attribute["key"] == "http.status_code":
                                            parsed_info["http.status_code"] = attribute["value"]["intValue"]
                                        if attribute["key"] == "rpc.grpc.status_code":
                                            parsed_info["rpc.grpc.status_code"] = attribute["value"]["intValue"]
                                        if attribute["key"] == "http.url":
                                            parsed_info["http.url"] = attribute["value"]["stringValue"]
                                        if attribute["key"] == "rpc.method":
                                            parsed_info["rpc.method"] = attribute["value"]["stringValue"]
                                    except KeyError as e:
                                        print(f"Key is not found: {e}")
                                        continue

                                # event 발생 시 event key 내에 exception.message와 exception.stacktrace가 따로 있음
                                for event in span.get("events", []):
                                    for attribute in event.get("attributes", []):
                                        if attribute["key"] == "exception.message":
                                            parsed_info["exception.message"] = attribute["value"]["stringValue"]
                                        if attribute["key"] == "exception.stacktrace":
                                            parsed_info["exception.stacktrace"] = attribute["value"]["stringValue"]

                                # span이 여러개인 경우 list에 파싱 결과를 append하여 전달
                                parsing_trace_data_list.append(parsed_info)

                except json.JSONDecodeError as e:
                    print(f"Error parsing line: {e}")

                self.process_original_trace(main_dict, span, parsing_trace_data_list)
                print("================ original_span 파싱 end ================\n")
                print("* original_idx:", current_index)
                file_idx.idx["original_span"] = current_index + 1
                print("* original_span_parsed_end_dictionary:", trace_id.main_dict)
