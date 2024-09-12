import json, itertools, datetime
import time

from util.datetime_util import change_timenano_format
import variables.trace_id as trace_id

# 로그 데이터 파싱 및 필요한 key 값 추출
# JSON 파일을 읽어오기

# # main_dict 테스트용
# trace_id.main_dict["log_parser"] = ""


class LogParsing:

    def __init__(self, input_path, output_path, filtered_file_name, original_file_name, filtered_idx, original_idx):

        self.input_path = input_path
        self.output_path = output_path
        self.filtered_file_name = filtered_file_name
        self.original_file_name = original_file_name
        self.filtered_idx = filtered_idx
        self.original_idx = original_idx

    def process_filtered_log(self, main_dict, log_record, parsed_log):
        # 상태가 trace인가?
        print("상태가 trace인가?\n")
        print(main_dict)
        trace_status_entries = {key: value for key, value in main_dict.items() if
                                isinstance(value, dict) and value.get('status') == 'trace'}
        print(trace_status_entries)

        # main_dict에 상태값이 trace인가 (trace_status_entries 내에 main_dict가 존재하는가) (N)
        # main_dict에 존재하는 경우 필터링 -> original_logs
        if len(trace_status_entries) > 0:

            # 파싱된 로그와 딕셔너리에 있는 trace ID값이 일치 하는가 (Y)
            if log_record["traceId"] in trace_status_entries:
                print("파싱된 로그와 딕셔너리에 있는 trace ID값이 일치 하는가 (Y)\n")
                parsed_log["traceId"] = log_record["traceId"]
                main_dict[log_record["traceId"]]["status"] = "confirm"
                # filtered_logs.append(parsed_log)

            else:
                print("파싱된 로그와 딕셔너리에 있는 trace ID값이 일치 하는가 (N)\n")
                self.original_logparser()
                # pass

            # main_dict에 상태값이 trace인가 (N)
        # elif:
        #     print("main_dict에 상태값이 trace인가 (N)\n")

            # 파싱된 로그에 trace ID가 있는가? (Y)
            if "traceId" in log_record and log_record["traceId"] != "":
                print("파싱된 로그에 trace ID가 있는가? (Y)\n")

                # main_dict에 key가 있는가? (N)
                if log_record["traceId"] not in main_dict:
                    print("main_dict에 key가 있는가? (N)\n")
                    parsed_log["traceId"] = log_record["traceId"]
                    main_dict[log_record["traceId"]] = {"status": "log",
                                                        "parsing_data_log": parsed_log,
                                                        "retry": 0,
                                                        "mail": "N"}
                    print(main_dict)


                # main_dict에 key가 있는가? (Y)
                else:
                    print("# main_dict에 key가 있는가? (Y)\n")

                    # main_dict 상태값이 confirm인가? (Y)
                    if main_dict[log_record["traceId"]]["status"] == "confirm":
                        print("# main_dict 상태값이 confirm인가? (Y)? (Y)\n")
                        main_dict[log_record["traceId"]]["status"] = "complete"
                        main_dict[log_record["traceId"]]["parsing_data_log"] = parsed_log

                    # main_dict 상태값이 confirm인가? (N)
                    else:
                        print("# main_dict 상태값이 confirm인가? (N)? (Y)\n")
                        pass


            # 파싱된 로그에 trace ID가 있는가? (N)
            else:
                print("# 파싱된 로그에 trace ID가 있는가? (N)\n")
                pass

        # main_dict에 상태값이 trace인가 (trace_status_entries 내에 main_dict가 존재하는가) (Y)
        # main_dict에 존재하지 않은 경우 필터링
        elif len(trace_status_entries) > 0 and log_record["traceId"] in trace_status_entries:
            print("main_dict에 상태값이 trace인가 (trace_status_entries 내에 main_dict가 존재하는가) (Y)\n")

            # 파싱된 로그와 딕셔너리에 있는 trace ID값이 일치 하는가 (Y)
            if log_record["traceId"] in trace_status_entries:
                print("파싱된 로그와 딕셔너리에 있는 trace ID값이 일치 하는가 (Y)\n")
                parsed_log["traceId"] = log_record["traceId"]
                main_dict[log_record["traceId"]]["status"] = "confirm"
                # filtered_logs.append(parsed_log)

            else:
                print("파싱된 로그와 딕셔너리에 있는 trace ID값이 일치 하는가 (N)\n")
                self.original_logparser()
                # pass

        # main_dict에 상태값이 trace인가 (N)
        else:
            print("main_dict에 상태값이 trace인가 (N)\n")

            # 파싱된 로그에 trace ID가 있는가? (Y)
            if "traceId" in log_record and log_record["traceId"] != "":
                print("파싱된 로그에 trace ID가 있는가? (Y)\n")

                # main_dict에 key가 있는가? (N)
                if log_record["traceId"] not in main_dict:
                    print("main_dict에 key가 있는가? (N)\n")
                    parsed_log["traceId"] = log_record["traceId"]
                    main_dict[log_record["traceId"]] = {"status": "log",
                                                        "parsing_data_log": parsed_log,
                                                        "retry": 0,
                                                        "mail": "N"}
                    print(main_dict)


                # main_dict에 key가 있는가? (Y)
                else:
                    print("# main_dict에 key가 있는가? (Y)\n")

                    # main_dict 상태값이 confirm인가? (Y)
                    if main_dict[log_record["traceId"]]["status"] == "confirm":
                        print("# main_dict 상태값이 confirm인가? (Y)? (Y)\n")
                        main_dict[log_record["traceId"]]["status"] = "complete"
                        main_dict[log_record["traceId"]]["parsing_data_log"] = parsed_log

                    # main_dict 상태값이 confirm인가? (N)
                    else:
                        print("# main_dict 상태값이 confirm인가? (N)? (Y)\n")
                        pass


            # 파싱된 로그에 trace ID가 있는가? (N)
            else:
                print("# 파싱된 로그에 trace ID가 있는가? (N)\n")
                pass

    def process_original_log(self, main_dict, log_record, parsed_log):
        # 상태가 trace인가?
        print("상태가 trace인가?\n")
        print(main_dict)
        trace_status_entries = {key: value for key, value in main_dict.items() if
                                isinstance(value, dict) and value.get('status') == 'trace'}
        print(trace_status_entries)

        # main_dict에 상태값이 trace인가 (trace_status_entries 내에 main_dict가 존재하는가) (Y)
        if len(trace_status_entries) > 0:
            print("main_dict에 상태값이 trace인가 (trace_status_entries 내에 main_dict가 존재하는가) (Y)\n")

            # 원문로그에 해당 trace id 가 있는가 (Y)
            if log_record["traceId"] in trace_status_entries:
                print("원문로그에 해당 trace id 가 있는가 (Y)\n")
                parsed_log["traceId"] = log_record["traceId"]
                main_dict[log_record["traceId"]]["status"] = "confirm"
            else:
                # main_dict에 있는 해당 키의 리트라이 횟수가 3 미만인가
                print("main_dict에 있는 해당 키의 리트라이 횟수가 3 미만인가 (Y)\n")
                # trace_status_entries에서 retry 값을 1씩 증가
                for trace_id, trace_info in trace_status_entries.items():
                    if trace_info.get("retry", 0) < 3:  # retry가 3 미만일 때만 증가
                        trace_info["retry"] += 1
                        print(f"Trace ID: {trace_id}, Retry 증가: {trace_info['retry']}")
                    else:
                        trace_info["status"] = 'complete'
                        print(f"Trace ID: {trace_id}, Retry 횟수가 이미 3에 도달")

    def filtered_logparser(self):

        input_path = self.input_path
        file_name = self.filtered_file_name
        idx = self.filtered_idx


        with open(input_path + file_name, "r") as log_file:
            for current_index, line in enumerate(itertools.islice(log_file, idx, None), start=idx):
                main_dict = trace_id.main_dict

                # # 디버깅할 때 사용..
                # input()

                print("filtered_log_start")
                print(datetime.datetime.now())

                try:
                    log_data = json.loads(line.strip())
                    change_timenano_format(log_data)  # 시간 전처리 적용
                    print(log_data)
                    for resource_log in log_data.get('resourceLogs', []):
                        parsed_info = {
                            "container.id": None,
                            "os.description": None,
                            "process.command_line": None,
                            "service.name": None,
                            "telemetry.sdk.language": None,
                            "logRecords_severityText": None,
                            "logRecords_body_stringValue": None,
                            "traceId": None,
                            "observedTimeUnixNano": None,  # 새로운 시간 필드 추가
                        }

                        if "resource" in resource_log and "attributes" in resource_log["resource"]:
                            for attribute in resource_log["resource"]["attributes"]:
                                if attribute["key"] == "container.id":
                                    parsed_info["container.id"] = attribute["value"]["stringValue"]
                                elif attribute["key"] == "os.description":
                                    parsed_info["os.description"] = attribute["value"]["stringValue"]
                                elif attribute["key"] == "process.command_line":
                                    parsed_info["process.command_line"] = attribute["value"]["stringValue"]
                                elif attribute["key"] == "service.name":
                                    parsed_info["service.name"] = attribute["value"]["stringValue"]
                                elif attribute["key"] == "telemetry.sdk.language":
                                    parsed_info["telemetry.sdk.language"] = attribute["value"]["stringValue"]

                        for scope_log in resource_log.get("scopeLogs", []):
                            for log_record in scope_log.get("logRecords", []):
                                if "observedTimeUnixNano" in log_record:
                                    parsed_info["observedTimeUnixNano"] = log_record["observedTimeUnixNano"]
                                if "severityText" in log_record:
                                    parsed_info["logRecords_severityText"] = log_record["severityText"]
                                if "body" in log_record and "stringValue" in log_record["body"]:
                                    parsed_info["logRecords_body_stringValue"] = log_record["body"]["stringValue"]

                                self.process_filtered_log(main_dict, log_record, parsed_info)
                                print("============filtered===========\n")

                                print("parsed_filtered_log")
                                print("filtered_idx")
                                print(idx)  # idx

                                print("filterparsed_end_dictionary")
                                print(trace_id.main_dict)



                except json.JSONDecodeError as e:
                    print(f"Error parsing line: {e}")

    def original_logparser(self):

        input_path = self.input_path
        file_name = self.original_file_name
        idx = self.original_idx

        with open(input_path + file_name, "r") as log_file:
            for current_index, line in enumerate(itertools.islice(log_file, idx, None), start=idx):
                main_dict = trace_id.main_dict

                # # 디버깅할 때 사용 ..
                # input()

                print("original_log_start")
                print(datetime.datetime.now())

                try:
                    log_data = json.loads(line.strip())
                    change_timenano_format(log_data)  # 시간 전처리 적용
                    print(log_data)
                    for resource_log in log_data.get('resourceLogs', []):
                        parsed_info = {
                            "container.id": None,
                            "os.description": None,
                            "process.command_line": None,
                            "service.name": None,
                            "telemetry.sdk.language": None,
                            "logRecords_severityText": None,
                            "logRecords_body_stringValue": None,
                            "traceId": None,
                            "observedTimeUnixNano": None,  # 새로운 시간 필드 추가
                        }

                        if "resource" in resource_log and "attributes" in resource_log["resource"]:
                            for attribute in resource_log["resource"]["attributes"]:
                                if attribute["key"] == "container.id":
                                    parsed_info["container.id"] = attribute["value"]["stringValue"]
                                elif attribute["key"] == "os.description":
                                    parsed_info["os.description"] = attribute["value"]["stringValue"]
                                elif attribute["key"] == "process.command_line":
                                    parsed_info["process.command_line"] = attribute["value"]["stringValue"]
                                elif attribute["key"] == "service.name":
                                    parsed_info["service.name"] = attribute["value"]["stringValue"]
                                elif attribute["key"] == "telemetry.sdk.language":
                                    parsed_info["telemetry.sdk.language"] = attribute["value"]["stringValue"]

                        for scope_log in resource_log.get("scopeLogs", []):
                            for log_record in scope_log.get("logRecords", []):
                                if "observedTimeUnixNano" in log_record:
                                    parsed_info["observedTimeUnixNano"] = log_record["observedTimeUnixNano"]
                                if "severityText" in log_record:
                                    parsed_info["logRecords_severityText"] = log_record["severityText"]
                                if "body" in log_record and "stringValue" in log_record["body"]:
                                    parsed_info["logRecords_body_stringValue"] = log_record["body"]["stringValue"]

                                self.process_original_log(main_dict, log_record, parsed_info)

                                # print(result)
                                print("============original===========\n")
                                print("parsed_original_log")
                                print("original_idx")
                                print(idx)  # idx

                                print("originalparsed_end_dictionary")
                                print(trace_id.main_dict)

                except json.JSONDecodeError as e:
                    print(f"Error parsing line: {e}")