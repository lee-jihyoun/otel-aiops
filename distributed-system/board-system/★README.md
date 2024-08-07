

## 개발 환경
- Gradle-8.8
- JAVA17
- H2 database
---
## DB 접속
- url : http://localhost:5050/h2-console
- Driver Class : org.h2.Driver
- JDBC URL: jdbc:h2:~/otel-agent
- User Name : sa
- Password :
---
## API 설명
- 로그 조회 : localhost:5050/log
- 로그 저장 : localhost:5050/log/save
- 게시글 전체 조회 : localhost:5050/board
- 게시글 수량 지정 조회 : localhost:5050/board/{count}
---


## 프로세스 흐름
1. 사용자(Client)가 Request를 보냄
2. Spring의 AOP의 @Before에서  기본적인 metric , Span  데이터 생성
3. Controller ~ Service 로직에서는 AOP에서 생성한 Span을 가져와서 하위(Child) Span을 생성
4. 모든 로직이 끝난 후에 AOP의 @After에서 생성한 Span을 종료
5. 사용자에게 Response 전달
---
## Data end point
- Span(trace) Data
    - Application -> OpenTelemetry collector -> Jaeger

- Metric
    - Application -> OpenTelemetry collector ->  Prometheus

- log
    - Application -> OpenTelemetry collector -> file & loki

## 실행 옵션
```shell
JAVA_TOOL_OPTIONS=-javaagent:..\..\opentelemetry-javaagent.jar
set OTEL_METRIC_EXPORT_INTERVAL=1000
set OTEL_TRACES_EXPORTER=otlp
set OTEL_METRICS_EXPORTER=otlp
set OTEL_LOGS_EXPORTER=otlp
set OTEL_SERVICE_NAME =board-system
set OTEL_EXPORTER_OTLP_ENDPOINT=http://127.0.0.1:9999
set OTEL_EXPORTER_OTLP_TRACES_ENDPOINT=http://127.0.0.1:9999
set OTEL_EXPORTER_OTLP_METRICS_ENDPOINT=http://127.0.0.1:9999
set OTEL_EXPORTER_OTLP_LOGS_ENDPOINT=http://127.0.0.1:9999
set OTEL_EXPORTER_OTLP_PROTOCOL=grpc
java -jar board-system-0.0.1-SNAPSHOT.jar
```

---
## FAQ
#### Springboot 애플리케이션에서는 아무것도 설정하지 않는가?
```text
SpringBoot 애플리케이션에서는 java , config , yml 등과 관련된 파일을 아무것도 수정하지 않고 사용
OpenTelemetry의 agent를 사용하여 계측하기 때문에 실행 시 옵션만 주면 됨
```

#### 환경변수 설정으로 계측할수 있는 부분은 어디까지 인가?
```text
https://opentelemetry.io/docs/languages/java/configuration/
위 링크에서 확인해보면 다양한 옵션들이 있으며, 계측 범위를 지정가능함
```

#### Jboss / Tomcat에도 적용이 가능 한가?
```text
적용가능함 [Otel]Tomcat Agent 적용.md 파일에 톰캣에 agent를 적용하여 테스트한 내용이 있음
톰캣의 설정파일 및 실행파일만을 수정하면 적용됨
```
---



## 기타 참고 링크

### Java Agent
- https://opentelemetry.io/docs/zero-code/java/agent/