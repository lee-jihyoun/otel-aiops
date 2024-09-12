import json, itertools
from util.datetime_util import change_timenano_format
import variables.trace_id as trace_id

# Trace_parser에서 할 일
# - filtered_span & original_span parsing
# - trace id 찾는 함수 : 500, error가 발생한 trace id를 찾기

# batch1
# 1. parsing_span()

# batch2
# 1. find_trace_id() -> return trace_ids {} / 500, error를 갖는 trace id 추출
# 2. extract_span_with_trace_id() / trace id에 맞는 span만 추출
# 3. parsing_span() / filtered_span, extraced_span 데이터 경우에 따라 make_parsed_info()를 호출하는 함수
# 4. make_parsed_info() / parsed_info를 만드는 함수. 디테일한 파싱 작업 수행

class TraceParsing:

    def __init__(self, input_path, output_path, idx, file_name):
        self.input_path = input_path
        self.output_path = output_path
        self.file_name = file_name
        self.idx = idx

    def process_filtered_trace(self, main_dict, span, parsed_trace, filtered_traces):
        # 상태가 log인가?
        print("상태가 log인가?\n")
        trace_status_entries = {key: value for key, value in main_dict.items() if
                                isinstance(value, dict) and value.get('status') == 'log'}
        print(trace_status_entries)

        # main_dict에 상태값이 log인가 (trace_status_entries 내에 main_dict가 존재하는가) (Y)
        if len(trace_status_entries) > 0:
            print("main_dict에 상태값이 log인가 (trace_status_entries 내에 main_dict가 존재하는가) (Y)\n")

            # 파싱된 로그와 딕셔너리에 있는 trace ID값이 일치 하는가 (Y)
            if span["traceId"] in trace_status_entries:
                print("파싱된 트레이스와 딕셔너리에 있는 trace ID값이 일치 하는가 (Y)\n")
                parsed_trace["traceId"] = span["traceId"]
                main_dict[span["traceId"]]["status"] = "confirm"
                # filtered_traces.append(parsed_trace)

            else:
                print("파싱된 트레이스와 딕셔너리에 있는 trace ID값이 일치 하는가 (N)\n")
                pass

        # main_dict에 상태값이 log인가 (N)
        else:
            print("main_dict에 상태값이 log인가 (N)\n")

            # 파싱된 트레이스에 trace ID가 있는가? (Y)
            if "traceId" in span and span["traceId"] != "":
                print("파싱된 트레이스에 trace ID가 있는가? (Y)\n")

                # main_dict에 key가 있는가? (N)
                if span["traceId"] not in main_dict:
                    print("main_dict에 key가 있는가? (N)\n")
                    parsed_trace["traceId"] = span["traceId"]
                    filtered_traces.append(parsed_trace)
                    main_dict[span["traceId"]] = {"status": "trace",
                                                            "parsing_data_trace": parsed_trace,
                                                            "retry": 0,
                                                            "mail": "N"}


                # main_dict에 key가 있는가? (Y)
                else:
                    print("# main_dict에 key가 있는가? (Y)\n")

                    # main_dict 상태값이 confirm인가? (Y)
                    if main_dict[span["traceId"]]["status"] == "confirm":
                        print("# main_dict 상태값이 confirm인가? (Y)? (Y)\n")
                        main_dict[span["traceId"]]["status"] = "complete"
                        main_dict[span["traceId"]]["parsing_data_trace"] = parsed_trace

                    # main_dict 상태값이 confirm인가? (N)
                    else:
                        print("# main_dict 상태값이 confirm인가? (N)? (Y)\n")
                        pass


            # 파싱된 로그에 trace ID가 있는가? (N)
            else:
                print("# 파싱된 로그에 trace ID가 있는가? (N)\n")
                pass

    def process_original_trace(self, main_dict, span, parsed_trace, original_traces):
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
                parsed_trace["traceId"] = span["traceId"]
                main_dict[span["traceId"]]["status"] = "confirm"
                original_traces.append(parsed_trace)
            else:
                # main_dict에 있는 해당 키의 리트라이 횟수가 3 미만인가
                print("main_dict에 있는 해당 키의 리트라이 횟수가 3 미만인가 (Y)\n")
                # trace_status_entries에서 retry 값을 1씩 증가
                for trace_id, trace_info in trace_status_entries.items():
                    if trace_info.get("retry", 0) < 3:  # retry가 3 미만일 때만 증가
                        trace_info["retry"] += 1
                        print(f"Trace ID: {trace_id}, Retry 증가: {trace_info['retry']}")
                        break
                    else:
                        trace_info["status"] = 'confirm'
                        print(f"Trace ID: {trace_id}, Retry 횟수가 이미 3에 도달")

    def traceparser(self):
        result = []

        input_path = self.input_path
        file_name = self.file_name
        idx = self.idx
        main_dict = trace_id.main_dict

        existing_trace_ids_dict = main_dict
        print("existing_trace_ids_dict: ", existing_trace_ids_dict)  # main_dict 불러와서 저장

        with open(input_path + file_name, "r") as log_file:
            for current_index, line in enumerate(itertools.islice(log_file, idx, None), start=idx):
                try:
                    span_data = json.loads(line.strip())
                    change_timenano_format(span_data)

                    for resource in span_data.get('resourceSpans', []):
                        parsed_info = {
                            "service.name": None,
                            "os.type": None,
                            "traceId": None,
                            "spanId": None,
                            "name": None,
                            "http.status_code": None,
                            "rpc.grpc.status_code": None,
                            "exception.message": None,
                            "exception.stacktrace": None,
                            "http.url": None,
                            "rpc.method": None,
                            "startTimeUnixNano": None,
                            "endTimeUnixNano": None
                        }

                        if "resource" in resource and "attributes" in resource["resource"]:
                            for attribute in resource["resource"]["attributes"]:
                                if attribute["key"] == "service.name":
                                    parsed_info["service.name"] = attribute["value"]["stringValue"]
                                if attribute["key"] == "os.type":
                                    parsed_info["os.type"] = attribute["value"]["stringValue"]

                        for scopeSpan in resource.get("scopeSpans", []):
                            for span in scopeSpan.get("spans", []):
                                if attribute["key"] == "traceId":
                                    parsed_info["traceId"] = span["traceId"]
                                if attribute["key"] == "spanId":
                                    parsed_info["spanId"] = span["spanId"]
                                if attribute["key"] == "name":
                                    parsed_info["name"] = span["name"]
                                if attribute["key"] == "startTimeUnixNano":
                                    parsed_info["startTimeUnixNano"] = span["startTimeUnixNano"]
                                if attribute["key"] == "endTimeUnixNano":
                                    parsed_info["endTimeUnixNano"] = span["endTimeUnixNano"]

                                for attribute in span.get("attributes", []):
                                    try:
                                        if attribute["key"] == "http.status_code":
                                            parsed_info["http.status_code"] = attribute["value"]["intValue"]
                                        elif attribute["key"] == "rpc.grpc.status_code":
                                            parsed_info["rpc.grpc.status_code"] = attribute["value"]["intValue"]
                                        elif attribute["key"] == "http.url":
                                            parsed_info["http.url"] = attribute["value"]["stringValue"]
                                        elif attribute["key"] == "rpc.method":
                                            parsed_info["rpc.method"] = attribute["value"]["stringValue"]
                                    except KeyError as e:
                                        print(f"Key is not found: {e}")
                                        continue

                                for event in span.get("events", []):
                                    for attribute in event.get("attributes", []):
                                        if attribute["key"] == "exception.message":
                                            parsed_info["exception.message"] = attribute["value"]["stringValue"]
                                        elif attribute["key"] == "exception.stacktrace":
                                            parsed_info["exception.stacktrace"] = attribute["value"]["stringValue"]

                                        if self.file_name == 'filtered_span.json':
                                            self.process_filtered_trace(main_dict, span, parsed_info, result)

                                        else:
                                            self.process_original_trace(main_dict, span, parsed_info, result)

                except json.JSONDecodeError as e:
                    print(f"Error parsing line: {e}")

        print("new_idx: ", idx)
        return idx, result