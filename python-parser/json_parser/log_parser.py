import json, itertools, datetime
from util.datetime_util import change_timenano_format
import variables.trace_id as trace_id
import variables.file_idx as file_idx
import logging


class LogParsing:

    def __init__(self, input_path, filtered_file_name, original_file_name, filtered_idx, original_idx):

        self.input_path = input_path
        self.filtered_file_name = filtered_file_name
        self.original_file_name = original_file_name
        self.filtered_idx = filtered_idx
        self.original_idx = original_idx

    def process_filtered_log(self, main_dict, log_record, parsed_log):

        print(parsed_log)
        # 상태가 trace인가?
        logging.info("상태가 trace인가?\n")
        logging.info(f"* main_dict: {main_dict}")
        trace_status_entries = {key: value for key, value in main_dict.items() if
                                isinstance(value, dict) and value.get('status') == 'trace'}

        # main_dict에 상태값이 trace인가 (trace_status_entries 내에 main_dict가 존재하는가) (N)
        # main_dict에 존재하는 경우 필터링 -> original_logs
        if len(trace_status_entries) > 0:

            # 파싱된 로그와 딕셔너리에 있는 trace ID값이 일치 하는가 (Y)
            if log_record["traceId"] in trace_status_entries:
                logging.info("파싱된 로그와 딕셔너리에 있는 trace ID값이 일치 하는가 (Y)\n")
                matching_log = [data for data in parsed_log if data.get("traceId") == log_record["traceId"]]
                if matching_log:
                    parsed_log["traceId"] = log_record["traceId"]
                    main_dict[log_record["traceId"]]["status"] = "confirm"
                    main_dict[log_record["traceId"]]["parsing_data_log"] = matching_log

            else:
                logging.info("파싱된 로그와 딕셔너리에 있는 trace ID값이 일치 하는가 (N)\n")
                self.original_logparser()
                # pass

            # 파싱된 로그에 trace ID가 있는가? (Y)
            if "traceId" in log_record and log_record["traceId"] != "":
                logging.info("파싱된 로그에 trace ID가 있는가? (Y)\n")

                # main_dict에 key가 있는가? (N)
                if log_record["traceId"] not in main_dict:
                    logging.info("main_dict에 key가 있는가? (N)\n")
                    for co_parsed_log in parsed_log:
                        co_parsed_log["traceId"] = log_record["traceId"]

                        main_dict[log_record["traceId"]] = {"status": "log",
                                                            "parsing_data_log": parsed_log,
                                                            "parsing_data_trace": "",
                                                            "retry": 0,
                                                            "mail": "N"}
                    logging.info(f"* main_dict: {main_dict}")

                # main_dict에 key가 있는가? (Y)
                else:
                    logging.info("# main_dict에 key가 있는가? (Y)\n")
                    logging.info(f"* main_dict: {main_dict}")

                    matching_log = [data for data in parsed_log if data.get("traceId") == log_record["traceId"]]
                    if matching_log:
                        parsed_log["traceId"] = log_record["traceId"]
                        main_dict[log_record["traceId"]]["status"] = "confirm"
                        main_dict[log_record["traceId"]]["parsing_data_log"] = matching_log

            # 파싱된 로그에 trace ID가 있는가? (N)
            else:
                logging.info("# 파싱된 로그에 trace ID가 있는가? (N)\n")
                pass

        # main_dict에 상태값이 trace인가 (trace_status_entries 내에 main_dict가 존재하는가) (Y)
        # main_dict에 존재하지 않은 경우 필터링
        elif len(trace_status_entries) > 0 and log_record["traceId"] in trace_status_entries:
            logging.info("main_dict에 상태값이 trace인가 (trace_status_entries 내에 main_dict가 존재하는가) (Y)\n")

            # 파싱된 로그와 딕셔너리에 있는 trace ID값이 일치 하는가 (Y)
            if log_record["traceId"] in trace_status_entries:
                logging.info("파싱된 로그와 딕셔너리에 있는 trace ID값이 일치 하는가 (Y)\n")
                matching_log = [data for data in parsed_log if data.get("traceId") == log_record["traceId"]]
                if matching_log:
                    parsed_log["traceId"] = log_record["traceId"]
                    main_dict[log_record["traceId"]]["status"] = "confirm"
                    main_dict[log_record["traceId"]]["parsing_data_log"] = matching_log

            else:
                logging.info("파싱된 로그와 딕셔너리에 있는 trace ID값이 일치 하는가 (N)\n")
                self.original_logparser()
                # pass

        # main_dict에 상태값이 trace인가 (N)
        else:
            logging.info("main_dict에 상태값이 trace인가 (N)\n")

            # 파싱된 로그에 trace ID가 있는가? (Y)
            if "traceId" in log_record and log_record["traceId"] != "":
                logging.info("파싱된 로그에 trace ID가 있는가? (Y)\n")

                # main_dict에 key가 있는가? (N)
                if log_record["traceId"] not in main_dict:
                    logging.info("main_dict에 key가 있는가? (N)\n")

                    for co_parsed_log in parsed_log:
                        co_parsed_log["traceId"] = log_record["traceId"]

                        main_dict[log_record["traceId"]] = {"status": "log",
                                                            "parsing_data_log": parsed_log,
                                                            "parsing_data_trace": "",
                                                            "retry": 0,
                                                            "mail": "N"}

                        logging.info(f"* main_dict: {main_dict}")

                # main_dict에 key가 있는가? (Y)
                else:
                    logging.info("# main_dict에 key가 있는가? (Y)\n")
                    matching_log = [data for data in parsed_log if data.get("traceId") == log_record["traceId"]]
                    if matching_log:
                        parsed_log["traceId"] = log_record["traceId"]
                        main_dict[log_record["traceId"]]["status"] = "confirm"
                        main_dict[log_record["traceId"]]["parsing_data_log"] = matching_log

                    pass

            # 파싱된 로그에 trace ID가 있는가? (N)
            else:
                logging.info("# 파싱된 로그에 trace ID가 있는가? (N)\n")
                pass

    def process_original_log(self, main_dict, log_record, parsed_log):
        # 상태가 trace인가?
        logging.info("상태가 trace인가?\n")
        trace_status_entries = {key: value for key, value in main_dict.items() if
                                isinstance(value, dict) and value.get('status') == 'trace'}

        # main_dict에 상태값이 trace인가 (trace_status_entries 내에 main_dict가 존재하는가) (Y)
        if len(trace_status_entries) > 0:
            logging.info("main_dict에 상태값이 trace인가 (trace_status_entries 내에 main_dict가 존재하는가) (Y)\n")

            # 원문로그에 해당 trace id 가 있는가 (Y)
            if log_record["traceId"] in trace_status_entries:
                logging.info("원문로그에 해당 trace id 가 있는가 (Y)\n")
                matching_log = [data for data in parsed_log if data.get("traceId") == log_record["traceId"]]
                if matching_log:
                    parsed_log["traceId"] = log_record["traceId"]
                    main_dict[log_record["traceId"]]["status"] = "confirm"
                    main_dict[log_record["traceId"]]["parsing_data_log"] = matching_log

            else:
                # main_dict에 있는 해당 키의 리트라이 횟수가 3 미만인가
                logging.info("main_dict에 있는 해당 키의 리트라이 횟수가 3 미만인가 (Y)\n")
                # trace_status_entries에서 retry 값을 1씩 증가
                for trace_id, trace_info in trace_status_entries.items():
                    if trace_info.get("retry", 0) < 3:  # retry가 3 미만일 때만 증가
                        trace_info["retry"] += 1
                        logging.info(f"Trace ID: {trace_id}, Retry 증가: {trace_info['retry']}")
                    else:
                        trace_info["status"] = 'confirm'
                        logging.info(f"Trace ID: {trace_id}, Retry 횟수가 이미 3에 도달")

    def filtered_logparser(self):
        input_path = self.input_path
        file_name = self.filtered_file_name
        idx = self.filtered_idx

        parsing_log_data_list = []

        with open(input_path + file_name, "r") as log_file:
            for current_index, line in enumerate(itertools.islice(log_file, idx, None), start=idx):
                main_dict = trace_id.main_dict

                # # 디버깅할 때 사용..
                # print('* 아무 글자나 입력:')
                # input()

                logging.info(f"================ filtered_log 파싱 start: {datetime.datetime.now()} ================")

                try:
                    log_data = json.loads(line.strip())
                    change_timenano_format(log_data)  # 시간 전처리 적용
                    for resource_log in log_data.get('resourceLogs', []):
                        parsed_info = {
                            "container.id": None,
                            "os.description": None,
                            "process.command_line": None,
                            "service.name": None,
                            "service.code": None,
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
                                if attribute["key"] == "os.description":
                                    parsed_info["os.description"] = attribute["value"]["stringValue"]
                                if attribute["key"] == "process.command_line":
                                    parsed_info["process.command_line"] = attribute["value"]["stringValue"]
                                if attribute["key"] == "service.name":
                                    parsed_info["service.name"] = attribute["value"]["stringValue"]
                                if attribute["key"] == "service.code":
                                    parsed_info["service.code"] = attribute["value"]["stringValue"]
                                if attribute["key"] == "telemetry.sdk.language":
                                    parsed_info["telemetry.sdk.language"] = attribute["value"]["stringValue"]

                        for scope_log in resource_log.get("scopeLogs", []):
                            for log_record in scope_log.get("logRecords", []):
                                print("log_record")
                                print(log_record)
                                if "observedTimeUnixNano" in log_record:
                                    parsed_info["observedTimeUnixNano"] = log_record["observedTimeUnixNano"]
                                if "severityText" in log_record:
                                    parsed_info["logRecords_severityText"] = log_record["severityText"]
                                if "body" in log_record and "stringValue" in log_record["body"]:
                                    parsed_info["logRecords_body_stringValue"] = log_record["body"]["stringValue"]

                            parsing_log_data_list.append(parsed_info)

                except json.JSONDecodeError as e:
                    logging.ERROR(f"Error parsing line: {e}")

                self.process_filtered_log(main_dict, log_record, parsing_log_data_list)
                logging.info("============ filtered log 파싱 end ===========\n")
                logging.info(f"* filtered_idx: {current_index}")
                file_idx.idx["filtered_logs"] = current_index + 1
                logging.info(f"* filter_log_parsed_end_dictionary: {trace_id.main_dict}")

    def original_logparser(self):
        input_path = self.input_path
        file_name = self.original_file_name
        idx = self.original_idx

        parsing_log_data_list = []

        with open(input_path + file_name, "r") as log_file:
            for current_index, line in enumerate(itertools.islice(log_file, idx, None), start=idx):
                main_dict = trace_id.main_dict

                # # 디버깅할 때 사용 ..
                # print('* 아무 글자나 입력:')
                # input()

                logging.info(f"================ original_log 파싱 start: {datetime.datetime.now()} ================")

                try:
                    log_data = json.loads(line.strip())
                    change_timenano_format(log_data)  # 시간 전처리 적용
                    for resource_log in log_data.get('resourceLogs', []):
                        parsed_info = {
                            "container.id": None,
                            "os.description": None,
                            "process.command_line": None,
                            "service.name": None,
                            "service.code": None,
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
                                if attribute["key"] == "os.description":
                                    parsed_info["os.description"] = attribute["value"]["stringValue"]
                                if attribute["key"] == "process.command_line":
                                    parsed_info["process.command_line"] = attribute["value"]["stringValue"]
                                if attribute["key"] == "service.name":
                                    parsed_info["service.name"] = attribute["value"]["stringValue"]
                                if attribute["key"] == "service.code":
                                    parsed_info["service.code"] = attribute["value"]["stringValue"]
                                if attribute["key"] == "telemetry.sdk.language":
                                    parsed_info["telemetry.sdk.language"] = attribute["value"]["stringValue"]

                        for scope_log in resource_log.get("scopeLogs", []):
                            for log_record in scope_log.get("logRecords", []):
                                if "observedTimeUnixNano" in log_record:
                                    parsed_info["observedTimeUnixNano"] = log_record["observedTimeUnixNano"]
                                if "severityText" in log_record:
                                    parsed_info["logRecords_severityText"] = log_record["severityText"]
                                if "body" in log_record and "stringValue" in log_record["body"]:
                                    parsed_info["logRecords_body_stringValue"] = log_record["body"]["stringValue"]

                            parsing_log_data_list.append(parsed_info)

                except json.JSONDecodeError as e:
                    logging.ERROR(f"Error parsing line: {e}")

                self.process_original_log(main_dict, log_record, parsing_log_data_list)
                logging.info("============ original log 파싱 end ===========\n")
                logging.info(f"* original_idx: {current_index}")
                file_idx.idx["original_logs"] = current_index + 1
                logging.info(f"* original_parsed_end_dictionary: {trace_id.main_dict}")
