@echo off
rem Springboot build with gradle

echo ## gradlew.bat assemble
gradlew.bat assemble&& cd .\build\libs&& set JAVA_TOOL_OPTIONS=-javaagent:..\..\opentelemetry-javaagent.jar&& set OTEL_METRIC_EXPORT_INTERVAL=1000&& set OTEL_TRACES_EXPORTER=otlp&& set OTEL_METRICS_EXPORTER=otlp&& set OTEL_LOGS_EXPORTER=otlp&& set OTEL_SERVICE_NAME =board-system&& set OTEL_EXPORTER_OTLP_ENDPOINT=http://127.0.0.1:9999&& set OTEL_EXPORTER_OTLP_TRACES_ENDPOINT=http://127.0.0.1:9999&& set OTEL_EXPORTER_OTLP_METRICS_ENDPOINT=http://127.0.0.1:9999&& set OTEL_EXPORTER_OTLP_LOGS_ENDPOINT=http://127.0.0.1:9999&& set OTEL_EXPORTER_OTLP_PROTOCOL=grpc&& java -jar board-system-0.0.1-SNAPSHOT.jar

rem Run SpringBoot
rem echo ## cd .\build\libs&& java -jar board-system-0.0.1-SNAPSHOT.jar
