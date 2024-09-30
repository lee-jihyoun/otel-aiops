import logging

# 로그 설정
'''
DEBUG: 프로그램 작동에 대한 상세한 정보를 나타내는 로그로 문제의 원인을 파악할 때 사용
INFO: 프로그램 작동이 예상대로 진행되고 있는지 파악하기 위해 사용
WARNING: 추후에 발생 가능한 문제를 나타내기 위해 사용
ERROR : 프로그램이 의도한 기능을 수행하지 못하고 있는 상황을 나타내기 위해 사용
CRITICAL : 프로그램 실행 자체가 중단될 수 있음을 나타내기 위해 사용
'''

def setup_logging():
    # 로거 설정
    logger = logging.getLogger()
    logger.setLevel(logging.INFO)

    # 파일 핸들러 설정
    file_handler = logging.FileHandler("python-parser.log")
    file_handler.setFormatter(logging.Formatter("[%(asctime)s | %(levelname)s] %(message)s", datefmt="%Y-%m-%d %H:%M:%S"))
    logger.addHandler(file_handler)

    # 콘솔 핸들러 설정
    console_handler = logging.StreamHandler()
    console_handler.setFormatter(logging.Formatter("[%(asctime)s | %(levelname)s] %(message)s", datefmt="%Y-%m-%d %H:%M:%S"))
    logger.addHandler(console_handler)