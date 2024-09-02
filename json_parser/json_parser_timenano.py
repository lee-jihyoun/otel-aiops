import json
from datetime import datetime, timezone
import pytz

# 경로 설정
json_file_path = "./data/adServiceFailure/filtered_logs.json"
output_file_path = './data/adServiceFailure/output/filtered_logs.json'

# JSON 파일을 읽어오기
# 원 데이터는 json이 여러개 있는 구조여서 하나씩 라인을 읽어와서 리스트에 넣어줌
json_data = []
with open(json_file_path, "r") as json_file:
    for line in json_file:
        try:
            data = json.loads(line.strip())
            json_data.append(data)
        except json.JSONDecodeError as e:
            print(f"Error parsing line: {e}")

# print(json_data[0])

# 나노초를 datetime으로 변환하는 함수
def convert_nano_to_datetime(nano_time):
    # 나노초를 초로 변환
    seconds = nano_time // 1000000000
    # 초를 utc 시간대로 변환
    utc_dt = datetime.fromtimestamp(seconds, tz=timezone.utc)
    # utc 시간대를 korea 시간대로 변환
    kst_tz = pytz.timezone('Asia/Seoul')
    kst_dt = utc_dt.astimezone(kst_tz)
    # 원하는 형식으로 포맷 맞추기
    return kst_dt.strftime('%Y-%m-%d %H:%M:%S')

# json의 timenano 키의 값을 datetime으로 변환하는 함수. 재귀적으로 key를 찾는다.
def change_timenano_format(first_json):
    if isinstance(first_json, dict):
        for k, v in first_json.items():
            if k in ["timeUnixNano", "startTimeUnixNano", "observedTimeUnixNano", "endTimeUnixNano"]:
                formatted_time = convert_nano_to_datetime(int(v))
                # print(f"{k}: {formatted_time}")
                first_json[k] = formatted_time
            else:
                change_timenano_format(v);
    elif isinstance(first_json, list):
        for item in first_json:
            change_timenano_format(item)
    else:
        return

change_timenano_format(json_data);
print(json_data)

# 수정된 json 파일 저장
with open(output_file_path, 'w') as f:
    json.dump(json_data, f)
