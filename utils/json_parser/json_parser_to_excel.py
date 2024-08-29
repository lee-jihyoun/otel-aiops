import json
import pandas as pd
import openpyxl

# JSON 파일을 읽어오기
json_file_path = "traces.json"
with open(json_file_path, "r") as json_file:
    json_data = json.load(json_file)

# JSON 데이터를 평탄화하는 함수
def flatten_json(nested_json, parent_key='', sep='/'):
    items = []
    if isinstance(nested_json, dict):
        for k, v in nested_json.items():
            new_key = f"{parent_key}{sep}{k}" if parent_key else k
            items.extend(flatten_json(v, new_key, sep=sep).items())
    elif isinstance(nested_json, list):
        for i, v in enumerate(nested_json):
            new_key = f"{parent_key}{sep}{i}"
            items.extend(flatten_json(v, new_key, sep=sep).items())
    else:
        items.append((parent_key, nested_json))
    return dict(items)

# 평탄화된 JSON 데이터
flattened_json = flatten_json(json_data)

# 각 경로를 '/'로 나누어 depth를 추가
df = pd.DataFrame(flattened_json.items(), columns=['Path', 'Value'])

# Path를 '/'로 나눠서 여러 컬럼으로 분할
path_splits = df['Path'].str.split('/', expand=True)

# 원래 데이터프레임에 분할된 경로를 추가
final_df = pd.concat([path_splits, df['Value']], axis=1)

# 빈 컬럼을 제거하고, Excel 파일로 저장
final_df.to_excel("metrics.xlsx", index=False, header=False)
