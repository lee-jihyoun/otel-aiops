# OTLP HTTP Listener

## 목차

## 목적
-  Opentelemetry Collector 에서 otlp http로 export 데이터를 수신  

## 환경
- JDK 17.0.2
- Springboot 3.3.2


## swagger ui 접속
- http://localhost:13030/swagger-ui/index.html

## API 설명

- POST /otlp/protobuf/v1/traces
- - Protocol Buffers 타입의 trace 데이터 수집
- - collector config 파일에서 exporter의 encoding을 지정하지 않을 경우 사용 


- POST /otlp/protobuf/v1/metrics
- - Protocol Buffers 타입의 metric 데이터 수집
- - collector config 파일에서 exporter의 encoding을 지정하지 않을 경우 사용


- POST /otlp/protobuf/v1/logs
- - Protocol Buffers 타입의 log 데이터 수집
- - collector config 파일에서 exporter의 encoding을 지정하지 않을 경우 사용


- POST /otlp/json/v1/traces
- - json 타입의 trace 데이터 수집
- - collector config 파일에서 exporter의 encoding을 json으로 지정하였을 경우 사용


- POST /otlp/json/v1/metrics
- - json 타입의 metric 데이터 수집
- - collector config 파일에서 exporter의 encoding을 지정하지 않을 경우 사용


- POST /otlp/json/v1/logs
- - json 타입의 log 데이터 수집
- - collector config 파일에서 exporter의 encoding을 지정하지 않을 경우 사용


## 구현 방법


## 구현 클래스

### Controller
#### 메서드

### Service
#### 메서드

## 기타 참고 사항

