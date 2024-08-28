## tailscale 설치(appstore, curl 명령어로 설치, 패키지로 설치 등 다양한 방법이 있는데 패키지 방법을 권장) 
https://pkgs.tailscale.com/stable/#macos

## tailscale 활성화
systemctl enable 


## 맥에서 tailscale 세팅
https://tailscale.com/kb/1080/cli?tab=macos

## alias 추가
# 파일 열기
vi ~/.zshrc

# 아래의 별칭 추가
alias tailscale="/Applications/Tailscale.app/Contents/MacOS/Tailscale"

# 변경사항 반영
source ~/.zshrc



## tailscale 멤버 추가
지현이가 설정에서 멤버로 나의 이메일 추가

## tailscale 머신 share 추가
내 머신에서 share 누르고 지현이 gmail 계정 추가

## 서버에서 머신 share 추가
서버에서 share 누르고 gmail 계정 추가

## 서버와 다른 네트워크일때 ssh로 접속하기
ssh rnp@100.83.227.59


## tailscale 명령어
# 시작
tailscale up

# 종료
tailscale down

# 상태 확인
tailscale status