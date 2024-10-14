
# 아래의 스크립트로 실행
※ opentelemetry-javaagent.jar 는 같은 디렉토리에 넣어놓을것
vi start_reporting_service.sh

=====================================================================
#!/bin/bash

# OpenTelemetry 에이전트와 서비스 설정
export JAVA_TOOL_OPTIONS="-javaagent:./opentelemetry-javaagent.jar"
export OTEL_METRIC_EXPORT_INTERVAL=1000
export OTEL_TRACES_EXPORTER=otlp
export OTEL_METRICS_EXPORTER=otlp
export OTEL_LOGS_EXPORTER=otlp
export OTEL_SERVICE_NAME=spring-reporting-service
export OTEL_EXPORTER_OTLP_ENDPOINT=http://localhost:32784
export OTEL_EXPORTER_OTLP_TRACES_ENDPOINT=http://localhost:32784
export OTEL_EXPORTER_OTLP_METRICS_ENDPOINT=http://localhost:32784
export OTEL_EXPORTER_OTLP_LOGS_ENDPOINT=http://localhost:32784
export OTEL_EXPORTER_OTLP_PROTOCOL=grpc

# Spring Boot 애플리케이션 실행 (백그라운드에서 실행)
#nohup java -jar spring-reporting-service-0.0.1-SNAPSHOT.jar > spring-reporting-service.log 2>&1 &
nohup java -jar spring-reporting-service-0.0.1-SNAPSHOT.jar --spring.profiles.active=server > spring-reporting-service.log 2>&1 &

=====================================================================


# 아래 코드는 service.name 과 service.code추가
=====================================================================
#!/bin/bash
# OpenTelemetry 에이전트와 서비스 설정

JASYPT_ENCRYPTOR_PASSWORD=ktds.dsquare \
JAVA_TOOL_OPTIONS="-javaagent:/opt/Dsquare/opentelemetry-javaagent.jar \
-Dotel.resource.attributes=service.name=Dsquare,service.code=ds1001" \
OTEL_METRIC_EXPORT_INTERVAL=1000 \
OTEL_TRACES_EXPORTER=otlp \
OTEL_METRICS_EXPORTER=otlp \
OTEL_LOGS_EXPORTER=otlp \
OTEL_SERVICE_NAME=DSquare \
OTEL_EXPORTER_OTLP_ENDPOINT=http://127.0.0.1:4317 \
OTEL_EXPORTER_OTLP_TRACES_ENDPOINT=http://127.0.0.1:4317 \
OTEL_EXPORTER_OTLP_METRICS_ENDPOINT=http://127.0.0.1:4317 \
OTEL_EXPORTER_OTLP_LOGS_ENDPOINT=http://127.0.0.1:4317 \
OTEL_EXPORTER_OTLP_PROTOCOL=grpc \
nohup java -jar DSquare-User-0.0.1-SNAPSHOT.jar > output.log 2>&1 &
=====================================================================
