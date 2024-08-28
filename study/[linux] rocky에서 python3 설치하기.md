## dnf list로 설치 가능한 버전 조회
    dnf list python3.12

## python3.9 설치
    dnf install -y python3.12        

## python 버전 확인
    - 설치된 모든 파이썬 버전 확인하기
    ===========================
    [root@localhost profile.d]#  ls /usr/bin/python*
    /usr/bin/python3  /usr/bin/python3.12  /usr/bin/python3.6  /usr/bin/python3.6m
    ===========================

## python 3.9 모듈 설치
    python3.9 -m pip install <module>

    - 설치된 모듈 조회
    python3.9 -m pip list


    - 파이썬 설치 경로 확인
    which python3.9
    ===========================
    [root@localhost rnp]# which python3.9
    /usr/bin/python3.9
    ===========================



## python은 linux의 basic s/w가 되어서 함부로 삭제하면 난리가 난다고 함. 버전업을 하는 경우는 한가지임
    - 버전업할 python을 새로 설치
    - linux의 기본 프로그램을 새 python으로 변경
    - 이전 python 버전 삭제

## linux 기본 python 버전 변경하기
    - 경로명은 사용자의 시스템 환경에 따라 달라질 수 있음.
    update-alternatives --install /usr/bin/python python /usr/bin/python3.12

    ===========================
    [root@localhost profile.d]# update-alternatives --install /usr/bin/python python /usr/bin/python3.12
    대체 버전 1.19.2 - Copyright (C) 2001 Red Hat, Inc.
    GNU Public License하에 이 프로그램을
    자유롭게 재배포 할 수 있습니다.
    ===========================


    - 아래 명령을 실행하면 python version이 보임. 원하는 버전의 번호를 선택.
    ===========================
    [root@localhost profile.d]# update-alternatives --config python

    4 개의 프로그램이 'python'를 제공합니다.

    선택    명령
    -----------------------------------------------
    *+ 1           /usr/libexec/no-python
    2           /usr/bin/python3
    3           /usr/bin/python3.9
    4           /usr/bin/python3.12

    현재 선택[+]을 유지하려면 엔터키를 누르고, 아니면 선택 번호를 입력하십시오:4
    [root@localhost profile.d]# python --version
    Python 3.12.3
    ===========================

## 이전 Python 버전 삭제
    dnf remove python3.9
    
    ===========================
    [root@localhost profile.d]# dnf remove python3.9
    종속성이 해결되었습니다.
    ======================================================================================================================================================
    꾸러미                                   구조                  버전                                                  저장소                     크기
    ======================================================================================================================================================
    삭제 중:
    python39                                 x86_64                3.9.19-1.module+el8.10.0+1809+41195054                @appstream                 24 k
    사용하지 않는 종속 꾸러미 제거:
    python39-libs                            x86_64                3.9.19-1.module+el8.10.0+1809+41195054                @appstream                 32 M
    python39-pip                             noarch                20.2.4-9.module+el8.10.0+1721+e52d6351                @appstream                7.8 M
    python39-pip-wheel                       noarch                20.2.4-9.module+el8.10.0+1721+e52d6351                @appstream                1.1 M
    python39-setuptools                      noarch                50.3.2-5.module+el8.10.0+1582+bc278001                @appstream                3.8 M
    python39-setuptools-wheel                noarch                50.3.2-5.module+el8.10.0+1582+bc278001                @appstream                550 k

    연결 요약
    ======================================================================================================================================================
    삭제  6 꾸러미
    ===========================



## pip 업그레이드
    - pip는 python2 버전의 패키지 매니저. pip3는 python3 버전의 패키지 매니저.
    - pip는 자주 업데이트되기 때문에 자주 업데이트하는게 좋다.
    pip3 install --upgrade pip
