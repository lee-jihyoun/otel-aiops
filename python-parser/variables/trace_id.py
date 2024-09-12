global main_dict
main_dict = {"a111":
                     {"status": "true",
                      "retry": 0,
                      "mail": "N"},
                 "f7d3a0def428ecd662f6e721e56865ba":
                     {"status": "trace",
                      "retry": 0,
                      "mail": "N"},
                 "b222":
                     {"status": "trace",
                      "retry": 0,
                      "mail": "N"},
                 "c111":
                     {"status": "log",
                      "retry": 0,
                      "mail": "N"}
                 }
print("trace_id.py main_dict: ", main_dict)
print(main_dict["a111"]["status"])