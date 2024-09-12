import time, datetime
import json_parser.log_parser as log_parser
import json_parser.trace_parser as trace_parser
import variables.trace_id as trace_id
import variables.file_idx as file_idx

# # main_dict 테스트용
# trace_id.main_dict["total_batch"] = ""

def run_batch1():


    while True:
        # 경로 설정
        input_path = '../data/testfolder/'
        output_path = '../data/testfolder/output/'

        print("############로그 시작############")
        filtered_log = 'filtered_logs.json'
        original_log = 'original_logs.json'

        filtered_idx = file_idx.idx.get('filtered_logs')
        original_idx = file_idx.idx.get('original_logs')

        print("filtered_log_start")
        print(datetime.datetime.now())
        filtered_log_parsing = log_parser.LogParsing(input_path=input_path,
                                                    output_path=output_path,
                                                    file_name=filtered_log,
                                                    idx=filtered_idx)

        parsed_filtered_log = filtered_log_parsing.filtered_logparser()

        # index 업데이트
        new_filtered_index = parsed_filtered_log[0]
        file_idx.idx[filtered_log[:-5]] = new_filtered_index

        print("parsed_filtered_log")
        print(parsed_filtered_log[0])  # idx
        print(parsed_filtered_log[1])  # filtered_log[]
        print("filterparsed_end_dictionary")
        print(trace_id.main_dict)

        print("original_log_start")
        if parsed_filtered_log[1] == []:
            original_log_parsing = log_parser.LogParsing(input_path=input_path,
                                                        output_path=output_path,
                                                        file_name=original_log,
                                                        idx=original_idx)

            parsed_original_log = original_log_parsing.original_logparser()

            new_original_index = parsed_original_log[0]
            file_idx.idx[filtered_log[:-5]] = new_original_index

            print("parsed_original_log")
            print(parsed_original_log[0])  # idx
            print(parsed_original_log[1])  # filtered_log[]
            print("originparsed_end_dictionary")
            print(trace_id.main_dict)

        print("end")
        print(datetime.datetime.now())
        #
        #
        # print("###########스팬 시작############")
        # filtered_span = 'filtered_span.json'
        # original_span = 'original_span.json'
        #
        # filtered_idx = file_idx.idx.get('filtered_span')
        # original_idx = file_idx.idx.get('original_span')
        #
        # print("filtered_span_start")
        # print(datetime.datetime.now())
        # filtered_span_parsing = trace_parser.TraceParsing(input_path=input_path,
        #                                             output_path=output_path,
        #                                             file_name=filtered_span,
        #                                             idx=filtered_idx)
        #
        # parsed_filtered_span = filtered_span_parsing.traceparser()
        # time.sleep(100000)
        # # index 업데이트
        # new_filtered_index = parsed_filtered_span[0]
        # file_idx.idx[filtered_span[:-5]] = new_filtered_index
        #
        # print("parsed_filtered_span")
        # print(parsed_filtered_span[0])  # idx
        # print(parsed_filtered_span[1])  # filtered_span[]
        # print("filterparsed_end_dictionary")
        # print(trace_id.main_dict)
        #
        # print("original_span_start")
        # if parsed_filtered_span[1] == []:
        #     original_span_parsing = trace_parser.TraceParsing(input_path=input_path,
        #                                                 output_path=output_path,
        #                                                 file_name=original_span,
        #                                                 idx=original_idx)
        #
        #     parsed_original_span = original_span_parsing.traceparser()
        #
        #     new_original_index = parsed_original_span[0]
        #     file_idx.idx[filtered_span[:-5]] = new_original_index
        #
        #     print("parsed_original_span")
        #     print(parsed_original_span[0])  # idx
        #     print(parsed_original_span[1])  # filtered_span[]
        #     print("originparsed_end_dictionary")
        #     print(trace_id.main_dict)

        print("end")
        print(datetime.datetime.now())




        time.sleep(100)