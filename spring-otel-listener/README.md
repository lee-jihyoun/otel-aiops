# OTLP HTTP Listener

## 목차

## 목적
- Opentelemetry Collector 에서 otlp http로 export 데이터를 수신  



## 환경
- JDK 17.0.2
- Springboot 3.3.2


## swagger ui 접속
- http://localhost:13030/swagger-ui/index.html

## 기본적인 설명
- Opentelemetry Collecotr에서 otlpHttp 로 내보낸 데이터를 수신하기 위해 개발
- 수신한 데이터는 gzip으로 압축되어 있으며 데이터의 압축을 풀은 후 저장 (collector 기본설정)
- collector에서 encoding을 지정하지 않으면 protobuf 타입으로 데이터가 내보내짐
 

## API 설명

- POST /otlp/protobuf/v1/traces
- DATA : byte[]
- - Protocol Buffers 타입의 trace 데이터 수집
- - collector config 파일에서 exporter의 encoding을 지정하지 않을 경우 사용 


- POST /otlp/protobuf/v1/metrics
- DATA : byte[]
- - Protocol Buffers 타입의 metric 데이터 수집
- - collector config 파일에서 exporter의 encoding을 지정하지 않을 경우 사용


- POST /otlp/protobuf/v1/logs
- DATA : byte[]
- - Protocol Buffers 타입의 log 데이터 수집
- - collector config 파일에서 exporter의 encoding을 지정하지 않을 경우 사용


- POST /otlp/json/v1/traces
- DATA : byte[]
- - json 타입의 trace 데이터 수집
- - collector config 파일에서 exporter의 encoding을 json으로 지정하였을 경우 사용


- POST /otlp/json/v1/metrics
- DATA : byte[]
- - json 타입의 metric 데이터 수집
- - collector config 파일에서 exporter의 encoding을 지정하지 않을 경우 사용


- POST /otlp/json/v1/logs
- DATA : byte[]
- - json 타입의 log 데이터 수집
- - collector config 파일에서 exporter의 encoding을 지정하지 않을 경우 사용


## 기타 참고 사항

### 참고 링크
- exporter 
- - https://docs.splunk.com/observability/en/gdi/opentelemetry/components/otlphttp-exporter.html

### otlp exporter 설정파일
- 프로젝트 내에 있는 otelcol-config.yml 파일 참고

### gzip로 압축 되어 있는 이유 
- https://github.com/open-telemetry/opentelemetry-collector/pull/4632
- 기본적으로 exporter에서 http/gRPC로 내보낸 데이터는 gzip 으로 압축되어 있음
- 아래의 옵션을 사용하여 gzip 압축을 끌 수 있음
```yaml
exporters:
  otlphttp:
    compression: none
```

### protobuf 타입의 listener가 있는 이유
- Opentelemetry Collecotr에서 otlp http exporter의 타입은 protobuf임
- 아래의 옵션을 주면 json 타입으로 export가 가능함
```yaml
exporters:
  otlphttp/traces:
    encoding: json
```

---
 
- Opentelemetry demo에서 발생한 로그를 수집하여 분석하기 위함
- 컨테이너 안에 생성되는 로그파일을 직접 접근하여 수신할 수 없어서, 콜렉터에서 익스포트함
- 콜렉터가 위치한 곳에 json parser를 위치한다면 굳이 사용할 필요가 없음

