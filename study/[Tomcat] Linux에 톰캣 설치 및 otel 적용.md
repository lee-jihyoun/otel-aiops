# 톰캣 압축 해제
	cd /home/rnp/
	tar -zxvf apache-tomcat-10.1.30.tar.gz

# 톰캣 디렉토리 이동
	cp  -r apache-tomcat-10.1.30 /opt/

# otel agent 톰캣 라이브러리 폴더로 복사
	cp /home/rnp/opentelemetry-javaagent.jar /opt/apache-tomcat-10.1.30/bin/opentelemetry-javaagent.jar


# 톰캣 포트번호 변경
	cd /opt/apache-tomcat-10.1.30/conf
	vi server.xml
	- 기존
	=====================================================================
		<Connector port="8080" protocol="HTTP/1.1"
				   connectionTimeout="20000"
				   redirectPort="8443"
				   maxParameterCount="1000"

	=====================================================================
	- 변경
	=====================================================================
		<Connector port="14040" protocol="HTTP/1.1"
				   connectionTimeout="20000"
				   redirectPort="14443"
				   maxParameterCount="1000"
	=====================================================================


# 방화벽에 톰캣 포트 추가
	※ 이미추가되어 있어서 실행은 하지 않음
	firewall-cmd --permanent --add-port=14040/tcp


# 톰캣 실행
	cd /opt/apache-tomcat-10.1.30/bin/
	./startup.sh

# 톰캣 접속
	http://100.83.227.59:14040/

# 톰캣 중지
	cd /opt/apache-tomcat-10.1.30/bin/
	./shutdown.sh

# 톰캣 실행파일 수정
	cd /opt/apache-tomcat-10.1.30/bin
	vi startup.sh

	=====================================================================
	# -----------------------------------------------------------------------------
	# Start Script for the CATALINA Server
	# -----------------------------------------------------------------------------
	# 여기밑에 바로 추가
	export CATALINA_OPTS="$CATALINA_OPTS -javaagent:opentelemetry-javaagent.jar"
	export CATALINA_OPTS="$CATALINA_OPTS -Dotel.resource.attributes=service.name=spring-reporting-service,service.namespace=TOMCAT,service.code=SL1001"
	export CATALINA_OPTS="$CATALINA_OPTS -Dspring.profiles.active=server"
	export OTEL_METRIC_EXPORT_INTERVAL=1000
	export OTEL_TRACES_EXPORTER=otlp
	export OTEL_METRICS_EXPORTER=otlp
	export OTEL_LOGS_EXPORTER=otlp
	export OTEL_SERVICE_NAME=spring-reporting-service
	export OTEL_EXPORTER_OTLP_ENDPOINT=http://127.0.0.1:4317
	export OTEL_EXPORTER_OTLP_TRACES_ENDPOINT=http://127.0.0.1:4317
	export OTEL_EXPORTER_OTLP_METRICS_ENDPOINT=http://127.0.0.1:4317
	export OTEL_EXPORTER_OTLP_LOGS_ENDPOINT=http://127.0.0.1:4317
	export OTEL_EXPORTER_OTLP_PROTOCOL=grpc
	=====================================================================

# 실행 후 로그 적재 확인
	cd /opt/spring-otel-listener-run/
	vi original_logs.json
	# SL1001로 검색해서 찾음
	=====================================================================
	{"key":"service.code","value":{"stringValue":"SL1001"}}		
	=====================================================================
# 톰캣 중지
	cd /opt/apache-tomcat-10.1.30/bin/
	./shutdown.sh

# 기존 ROOT 파일 백업
	cd /opt/apache-tomcat-10.1.30/webapps/
	mv ROOT ROOT_backup

# war 파일 복사
	cp /home/rnp/spring-reporting-service-0.0.1-SNAPSHOT.war /opt/apache-tomcat-10.1.30/webapps/ROOT.war

# 톰캣 시작
	cd /opt/apache-tomcat-10.1.30/bin/
	./startup.sh

# 접속 확인
	※ 500오류 뜨면됨
	http://100.83.227.59:14040/error/test01
	http://100.83.227.59:14040/error/test02
	http://100.83.227.59:14040/error/test03
	http://100.83.227.59:14040/error/test04
	http://100.83.227.59:14040/error/test05
	http://100.83.227.59:14040/error/test06
	http://100.83.227.59:14040/error/test07

# 톰캣 로그 확인
	/opt/apache-tomcat-10.1.30/logs
	tail -f catalina.out

# otel filter log 적재 확인
	cd /opt/spring-otel-listener-run/
	vi filtered_logs.json
	# SL1001로 검색해서 찾음
	=====================================================================
	{"key":"service.code","value":{"stringValue":"SL1001"}
	=====================================================================

# tomcat 서비스 상태 확인
    ps -ef |grep tomcat
    =====================================================================
    root     1935457       1  7 00:34 pts/5    00:00:26 /opt/jdk-17.0.2/bin/java -Djava.util.logging.config.file=/opt/apache-tomcat-10.1.30/conf/logging.properties -Djava.util.logging.manager=org.apache.juli.ClassLoaderLogManager -Djdk.tls.ephemeralDHKeySize=2048 -Djava.protocol.handler.pkgs=org.apache.catalina.webresources -Dorg.apache.catalina.security.SecurityListener.UMASK=0027 --add-opens=java.base/java.lang=ALL-UNNAMED --add-opens=java.base/java.io=ALL-UNNAMED --add-opens=java.base/java.util=ALL-UNNAMED --add-opens=java.base/java.util.concurrent=ALL-UNNAMED --add-opens=java.rmi/sun.rmi.transport=ALL-UNNAMED -javaagent:opentelemetry-javaagent.jar -Dotel.resource.attributes=service.name=spring-reporting-service,service.namespace=TOMCAT,service.code=SL1001 -Dspring.profiles.active=server -classpath /opt/apache-tomcat-10.1.30/bin/bootstrap.jar:/opt/apache-tomcat-10.1.30/bin/tomcat-juli.jar -Dcatalina.base=/opt/apache-tomcat-10.1.30 -Dcatalina.home=/opt/apache-tomcat-10.1.30 -Djava.io.tmpdir=/opt/apache-tomcat-10.1.30/temp org.apache.catalina.startup.Bootstrap start
    root     1949712 1742265  0 00:40 pts/5    00:00:00 grep --color=auto tomcat
    =====================================================================