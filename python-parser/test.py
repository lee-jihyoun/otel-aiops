import itertools

import itertools
import time

# 전역 변수 선언
last_index = 0


# 새로운 로그를 주기적으로 확인하는 함수
def monitor_file(input_file):
    global last_index
    with open(input_file, "r", encoding='utf-8') as log_file:
        # 파일의 총 줄 수 확인
        total_lines = sum(1 for _ in log_file)

        if last_index < total_lines:
            with open(input_file, "r", encoding='utf-8') as log_file:
                # 마지막 저장된 인덱스부터 파일을 읽음
                for current_index, line in enumerate(itertools.islice(log_file, last_index, None), start=last_index):
                    print(f"{current_index}: {line.strip()}")
                    # 마지막 인덱스 갱신
                    last_index = current_index
        else:
            print("새로운 로그가 없습니다.")


# 주기적으로 파일을 모니터링하는 while True 루프
while True:
    monitor_file("prompt_template.txt")  # 파일 경로
    time.sleep(5)  # 5초마다 파일을 다시 확인

# # 파일의 총 줄 수 확인
# with open("prompt_template.txt", "r", encoding='utf-8') as log_file:
#     total_lines = sum(1 for _ in log_file)
#
# # 원하는 인덱스부터 읽기
# start_index =
# if start_index < total_lines:
#     with open("prompt_template.txt", "r", encoding='utf-8') as log_file:
#         for current_index, line in enumerate(itertools.islice(log_file, start_index, None)):
#             print(f"{current_index + start_index}: {line.strip()}")
# else:
#     print(f"파일의 총 줄 수는 {total_lines} 줄입니다. {start_index} 줄부터 읽을 수 없습니다.")
