import os

def check_file_modified(filepath, last_modified_time):
    """파일이 변경되었는지 확인하는 함수"""
    current_modified_time = os.path.getmtime(filepath)
    if current_modified_time != last_modified_time:
        return True, current_modified_time
    return False, last_modified_time