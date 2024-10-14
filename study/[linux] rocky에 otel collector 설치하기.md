# 콜렉터 디렉토리 생성
mkdir /opt/otel_collector

# 콜렉터 다운로드
cd /opt/otel_collector
wget https://github.com/open-telemetry/opentelemetry-collector-releases/releases/download/v0.100.0/otelcol_0.100.0_linux_386.tar.gz

# 압축 해제
tar -zxvf otelcol_0.100.0_linux_386.tar.gz

# 콜렉터 설정파일 생성
vi customconfig.yaml
=====================================================================
```yaml
receivers:
  otlp:
    protocols:
      grpc:
        endpoint: 0.0.0.0:4317
      http:
        endpoint: 0.0.0.0:4318

exporters:
  logging:
    verbosity: detailed

  otlphttp/metrics:
    encoding: json
    endpoint: http://127.0.0.1:13030/otlp/original/json

  otlphttp/filtered_traces:
    encoding: json
    endpoint: http://127.0.0.1:13030/otlp/filtered/json

  otlphttp/filtered_logs:
    encoding: json
    endpoint: http://127.0.0.1:13030/otlp/filtered/json

  otlphttp/original_traces:
    encoding: json
    endpoint: http://127.0.0.1:13030/otlp/original/json

  otlphttp/original_logs:
    encoding: json
    endpoint: http://127.0.0.1:13030/otlp/original/json


processors:
  batch:
  filter/logs:
    logs:
      log_record:
        - 'severity_number < 10'

  filter/error_spans:
    traces:
      span:
        - 'status.code != 2'

service:
  pipelines:
    logs:
      receivers: [otlp]
      processors: [batch]
      exporters: [logging, otlphttp/original_logs]
    traces:
      receivers: [otlp]
      processors: [batch]
      exporters: [otlphttp/original_traces]
    metrics:
      receivers: [otlp]
      processors: [batch]
      exporters: [otlphttp/metrics]

    logs/filtered:
      receivers: [otlp]
      processors: [batch, filter/logs]
      exporters: [otlphttp/filtered_logs]

    traces/error:
      receivers: [otlp]
      processors: [filter/error_spans]
      exporters: [otlphttp/filtered_traces]
```

=====================================================================


#  콜렉터 실행파일 생성
vi start_otel_collector.sh
=====================================================================
#!/bin/bash

nohup ./otelcol --config customconfig.yaml  > collector.log 2>&1 &
=====================================================================

# 실행
./start_otel_collector.sh


# 프로세스 확인
[root@localhost otel_collector]# ps -ef |grep otelcol
root     2060841       1  1 23:28 pts/2    00:00:00 ./otelcol --config customconfig.yaml
root     2061143 1970794  0 23:29 pts/2    00:00:00 grep --color=auto otelcol


# 로그 확인
cd /opt/spring-otel-listener-run
