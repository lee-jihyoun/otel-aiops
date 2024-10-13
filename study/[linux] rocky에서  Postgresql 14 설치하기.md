## postgres 14.8 버전 설치 (출처: https://blife.tistory.com/23)

# PostgreSQL 최신 배포판 설치를 위해 dnf Repository를 연결
    dnf install -y https://download.postgresql.org/pub/repos/yum/reporpms/EL-8-x86_64/pgdg-redhat-repo-latest.noarch.rpm

# RockyLinux 8 배포판에 추가되어 있는 postgresql 모듈 사용중지
    dnf -qy module disable postgresql

# PostgreSQL 14 설치
    dnf repository를 활용해 배포된 최신 버전의 postgresql 14를 설치할 수 있습니다.
    명령어 실행시 설치에 필요한 dependency 패키지가 함께 설치됩니다.
    dnf install -y postgresql14-server

# PostgreSQL 14 DB 초기화 설치
    데이터베이스를 저장소를 postgresql-14-setup initdb 명령어를 통해 기본 설치위치인 /var/lib/pgsql/14/data 에 초기화 되어 설치됩니다.
    /usr/pgsql-14/bin/postgresql-14-setup initdb

# Systemd 서비스 등록
    PostgreSQL 서비스 자동 시작 및 systemd를 통한 제어를 위해 PostgreSQL 14 를 system 서비스에 적용시킨다.
    systemctl enable postgresql-14

# PostgreSQL 시작
    systemd 명령어를 통해 PostgreSQL 14 데이터베이스를 시작합니다.
    systemctl start postgresql-14

# PostgreSQL 종료
    system 종료 명령어를 통해 PostgreSQL 14 데이터베이스를 종료합니다.
    systemclt stop postgresql-14


# PostgreSQL 14 데이터베이스 생성
    접속계정 생성 및 접속
    PostgreSQL 14에 접속하려면 설치시 생성된 postgres 계정을 이용해야합니다.
    postgres 계정은 패스워드가 설정되어 있지 않음으로 로그인이 불가합니다.
    root 계정에서 su 로 이동하거나 postgres 계정의 패스워드를 생성하여 로그인하면 됩니다.

# PostgreSQL 접속
    특별히 PostgreSQL 접속 포트나 접속위치에 대한 변경을 하지 않았다면 기본 설정을 읽기 때문에 psql 명령어 만으로도 접속이 됩니다.
    psql

# postgresql은 기본적으로 postgres 라는 사용자명을 사용하므로 다음과같이 실행
    sudo -i -u postgres
    psql

# PostgreSQL 14 사용자 생성
    PostgreSQL 데이터베이스를 사용하기 위해 다음과 같이 일반 사용자를 생성합니다.
    create role seon with login nosuperuser password '***********'';


# 데이터베이스 생성
    psql에 접속하여 CREATE DATABASE 명령어를 통해 데이터베이스 생성이 가능합니다.
    dsquare라는 DB의 소유자는 postgres 인코딩 타입은 'UTF-8'
    create database dsquare with owner = postgres encoding = 'UTF8';
