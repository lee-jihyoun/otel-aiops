global main_dict
main_dict = {"a111":
                     {"status": "complete",
                      "parsing_data_log": "파싱된 로그 123",
                      "parsing_data_trace": "파싱된 트레이스 123",
                      "retry": 0,
                      "mail": "N"},
                 "f7d3a0def428ecd662f6e721e56865ba":
                     {"status": "log",
                      "parsing_data_log": "파싱된 로그 123",
                      "retry": 0,
                      "mail": "N"},
                 "b222":
                     {"status": "trace",
                      "retry": 0,
                      "parsing_data_trace": "파싱된 트레이스 123",
                      "mail": "N"},
                 "c111":
                     {"status": "log",
                      "parsing_data_log": "파싱된 로그 123",
                      "retry": 0,
                      "mail": "N"}
                 }
print("trace_id.py main_dict: ", main_dict)
print(main_dict["a111"]["status"])