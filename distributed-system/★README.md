
## 목적
"분산처리, 다양한 시스템 연동 ,짭퉁MSA" 일 경우의 트레이싱 테스트 


## 실행
start_distributed-system.bat

## 테스트 진행을 위한 API
- 아래의 API 호출 시 연관된 API 자동 호출
- board-system
    - http://localhost:10010/board



## 서비스 API 
- board-system
  - http://localhost:10010/board
  - Method : GET
  - Result : Boolean
- user-system
  - http://localhost:10020/user
  - Method : GET
  - Result : Boolean
- ldap-system
  - http://localhost:10030/ldap
  - Method : GET
  - Result : Boolean
- log-system
  - http://localhost:10040/log
  - Method : GET
  - Result : Boolean


## 데이터 흐름 순서
- board 서비스를 호출하면 user 서비스 호출
- user 서비스에서는 ldap 서비스와 log 서비스 호출
- board 
  - user 
    - ldap 
    - log


## 테스트 케이스

1. 정상케이스
- 모든 서비스 실행 후 http://localhost:10010/board 호출

2. 중간 서비스 장애 케이스
- ldap-system 서비스 중지 후 http://localhost:10010/board 호출

