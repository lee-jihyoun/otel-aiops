## python 가상환경 설정하기. 가상환경 활성화를 한 뒤에 사용이 가능하다. 
# venv라는 이름의 가상환경 생성
cd /opt/otel-aiops/python-parser
python -m venv venv

## 가상환경 활성화
# mac, linux OS인 경우
source venv/bin/activate

# window인 경우
가상환경이름\Scripts\activate

# 가상환경 라이브러리 일괄 설치(requirements.txt에 정리된 버전 설치)
pip install -r ./config/requirements.txt 

# 가상환경 비활성화
deactivate

# 가상환경 삭제
sudo rm -rf 가상환경이름