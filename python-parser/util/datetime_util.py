from datetime import datetime, timezone
import pytz

# 문자열을 datetime으로 변환하는 함수
def convert_string_to_datetime(str_time):
    date_format = '%Y-%m-%d %H:%M:%S'
    datetime_time = datetime.strptime(str_time, date_format)
    return datetime_time

# 나노초를 datetime으로 변환하는 함수
def convert_nano_to_datetime(nano_time):
    # 이미 datetime 객체인 경우 예외 처리
    if isinstance(nano_time, datetime):
        return nano_time.strftime('%Y-%m-%d %H:%M:%S')

    seconds = nano_time // 1000000000
    utc_dt = datetime.fromtimestamp(seconds, tz=timezone.utc)
    kst_tz = pytz.timezone('Asia/Seoul')
    kst_dt = utc_dt.astimezone(kst_tz)
    return kst_dt.strftime('%Y-%m-%d %H:%M:%S')

# json의 timenano 키의 값을 datetime으로 변환하는 함수. 재귀적으로 key를 찾음
def change_timenano_format(first_json):
    if isinstance(first_json, dict):
        for k, v in first_json.items():
            if k in ["timeUnixNano", "startTimeUnixNano", "observedTimeUnixNano", "endTimeUnixNano"]:
                formatted_time = convert_nano_to_datetime(int(v))
                first_json[k] = formatted_time
            else:
                change_timenano_format(v)
    elif isinstance(first_json, list):
        for item in first_json:
            change_timenano_format(item)
    else:
        return