## rocky는 RHEL의 버그까지 재현하겠다는 목표로 제작된 배포판 리눅스다.
    https://hahahax5.tistory.com/10

# 사전 패키지 설치
    - 설치는 인터넷이 가능한 환경에서 진행한다.

    - dnf-utils 설치
    ================================ 
    [root@localhost rnp]# dnf install -y dnf-utils
    마지막 메타자료 만료확인(0:10:40 이전): 2024년 08월 22일 (목) 오전 01시 24분 46초.
    종속성이 해결되었습니다.
    ================================ 



    - docker 레포지토리 추가
    ================================ 
    [root@localhost rnp]# dnf config-manager --add-repo https://download.docker.com/linux/centos/docker-ce.repo
    다음 위치에서 레포 추가 : https://download.docker.com/linux/centos/docker-ce.repo
    ================================ 

    - 리포리스트 확인
    ================================ 
    [root@localhost rnp]# dnf repolist -v
    적재된 플러그인: builddep, changelog, config-manager, copr, debug, debuginfo-install, download, generate_completion_cache, groups-manager, kpatch, needs-restarting, playground, repoclosure, repodiff, repograph, repomanage, reposync, system-upgrade
    DNF version: 4.7.0
    cachedir: /var/cache/dnf
    Docker CE Stable - x86_64    
    ================================ 


# docker 설치
    dnf로 install docker를 하면 오류가 발생함.
    충돌하는 패키지를 삭제하며 설치해야하기 때문에 --allowerasing 옵션을 사용해야 함.

    ================================ 
    [root@localhost rnp]# dnf install -y docker-ce --allowerasing
    마지막 메타자료 만료확인(0:00:30 이전): 2024년 08월 22일 (목) 오전 01시 36분 06초.
    종속성이 해결되었습니다.
    ================================ 

# 설치 확인 및 실행
    ================================ 
    [rnp@localhost ~]$ docker --version
    Docker version 26.1.3, build b72abbb


    [rnp@localhost ~]$ systemctl status docker
    ● docker.service - Docker Application Container Engine
    Loaded: loaded (/usr/lib/systemd/system/docker.service; disabled; vendor preset: disabled)
    Active: inactive (dead)
        Docs: https://docs.docker.com
    ================================ 

     
    - 서비스 enable 및 시작
    ================================ 
    [rnp@localhost ~]$ systemctl enable docker
    ==== AUTHENTICATING FOR org.freedesktop.systemd1.manage-unit-files ====
    Authentication is required to manage system service or unit files.
    Authenticating as: ktds
    Password: 
    ==== AUTHENTICATION COMPLETE ====
    Created symlink /etc/systemd/system/multi-user.target.wants/docker.service → /usr/lib/systemd/system/docker.service.
    ==== AUTHENTICATING FOR org.freedesktop.systemd1.reload-daemon ====
    Authentication is required to reload the systemd state.
    Authenticating as: ktds
    Password: 
    ==== AUTHENTICATION COMPLETE ====
    ================================ 


# 도커 컨테이너 재시작
docker stop <컨테이너아이디>
docker start <컨테이너아이디>

# 도커 컨테이너 내부로 접속
docker exec -it <컨테이너아이디> /bin/bash

# 컨테이너 종료
exit

## 사용하지 않는 시스템 자원 지우기
docker system prune -a -f

## 빌드 캐시 삭제
docker builder prune -f


## docker & spring-otel-listener 실행하기
경로: /opt/otel-aiops/spring-otel-listener/build/libs
jar 파일 실행: java -jar spring-otel-listener-0.0.1-SNAPSHOT.jar

