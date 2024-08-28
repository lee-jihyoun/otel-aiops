## 계정 생성



## 계정 삭제 



## 계정 홈 디렉토리 변경 (rnp 계정의 홈 디렉토리를 /opt/rnp -> /home/rnp로 변경하려는 상황)

# 현재 잘못된 홈 디렉토리 확인
    grep rnp /etc/passwd

    ================================ 
    [root@localhost opt]# grep rnp /etc/passwd
    rnp:x:974:973::/opt/rnp:/bin/bash
    ================================ 

# 새로운 디렉토리를 생성
    mkdir /home/rnp

# /etc/passwd 파일 수정
# /etc/passwd 파일은 사용자 계정 정보를 포함하여 홈 디렉토리 경로를 정의함. 
    vi /etc/passwd

    - 기존
    ================================    
    rnp:x:974:973::/opt/rnp:/bin/bash
    ================================

    - 수정
    ================================
    rnp:x:974:973::/home/rnp:/bin/bash
    ================================


# 홈 디렉토리에 파일이나 설정이 있는 경우, 새로운 디렉토리로 이동
    mv /opt/rnp /home/rnp

# 홈 디렉토리 소유권 변경
    chown -R rnp:rnp /home/rnp


# 사용자 세션 재시작
    사용자 세션을 종료하고 다시 로그인하고나 시스템을 재부팅함
    logout
    reboot 