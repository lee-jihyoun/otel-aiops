
# 키클락 다운로드
	- Dev-space 사용 버전 : 13.0.0
	https://github.com/keycloak/keycloak/releases/tag/13.0.1
	https://github.com/keycloak/keycloak/releases/tag/13.0.0

# Jenkins 다운로드
	- Dev-space 사용 버전 : 2.289.1
	https://updates.jenkins.io/download/war/
	https://updates.jenkins.io/download/war/2.289.1/jenkins.war
	- 윈도우용 다운로드
	https://get.jenkins.io/windows-stable/2.289.1/jenkins.msi


# Jenkins 버전 교체
	※ 아래 방법 안됨 혹시나 해봣는데 Dependency errors 한가득임

	- 기존 : 2.346.2
	- 변경 : 2.289.1
	1. Jenkins 다운로드
		URL : https://updates.jenkins.io/download/war/2.289.1/jenkins.war
	
	2. Jenkins 서비스 중지
		services.msc 
		윈도우 서비스에서 Jenkins 서비스 중지

	3. Jenkins 설치 디렉토리에서 war 파일 변경
		※ 붙여넣기 전 기존 war파일 백업		
		경로 : C:\Program Files\Jenkins
		다운받은 war파일을 해당 경로에 붙여넣기

	4. Jenkins 서비스 시작
		services.msc 
		윈도우 서비스에서 Jenkins 서비스 실행

# Jenkins 설치
	※ 윈도우에서 먼저 테스트 함
	※ 13번부터는 낮은 버전때매 발생하는 오류로 보임

	1. 기존 버전 제거
		제어판 - 프로그램 추가제거에서 젠킨스 제거

	2. ProgramData 에서 jenkins삭제
		경로 : C:\ProgramData\Jenkins
		위 디렉토리 자체를 삭제

	3. 설치 파일 다운로드
		https://get.jenkins.io/windows-stable/2.289.1/jenkins.msi 
	
	4. 설치 파일 실행

	5. 서비스 구동 계정은 Run service as LocalSystem (not recommended) 선택
	
	6. localhost:7070 접속

	7. Unlock Jenkins 이라는 메시지가 뜨면 아래의 파일에 적혀있는 암호를 입력
		C:\ProgramData\Jenkins\.jenkins\secrets\initialAdminPassword
	
	8. 아래의 메시지 출력됨
		=====================================================================
		Offline
		This Jenkins instance appears to be offline.
		=====================================================================
		참고링크 : https://stackoverflow.com/questions/42408703/why-does-jenkins-say-this-jenkins-instance-appears-to-be-offline
		
		SSL인증 오류라고 하니 아래의 파일 수정
		경로 : C:\ProgramData\Jenkins\.jenkins
		파일명 : hudson.model.UpdateCenter.xml
		수정내용 :  https 를 http 로 변경
		=====================================================================
		<?xml version='1.1' encoding='UTF-8'?>
		<sites>
		  <site>
			<id>default</id>
			<url>http://updates.jenkins.io/update-center.json</url>
		  </site>
		</sites>
		=====================================================================
	
	9. Jenkins 재시작
	
	10. Jenkins 접속
		localhost:7070
		7번항목이 다시뜨면 비번 똑같이 입력
	
	11. Customize Jenkins
		Install suggested plugins 선택
		※ 플러그인 전부다 설치 안됨, 그냥 넘어갈것
	
	12. 계정명 , 암호, 암호확인, 이름 은 알아서 입력


	13. 플러그인 설치 오류 해결
		참고링크 : https://sweet0828.tistory.com/16
		참고링크 : https://nevido.tistory.com/580

		아래의 링크에서 skip-certificate-check.hpi 다운로드
		※ 1.1버전은 2.346.3 버전이상이므로 1.0 버전 다운로드
		https://updates.jenkins-ci.org/download/plugins/skip-certificate-check/
		https://updates.jenkins-ci.org/download/plugins/skip-certificate-check/1.0/skip-certificate-check.hpi
	
	13-1. 플러그인 이동
		경로 : C:\ProgramData\Jenkins\.jenkins\plugins
		위 경로로 플러그인 이동

	13-2. 젠킨스 재시작
		그럼 이제 모든 플러그인이 설치되어 있음



# Jenkins에 오픈텔레메트리 에이전트 추가

	# 1안 - jenkins.xml 파일 수정

	※ 안됨 뭐가문젠지 보려고 하는데 windows 에서는 로그가 안남음
	=====================================================================
	<arguments>
	-Xrs 
	-Xmx256m 
	-Dhudson.lifecycle=hudson.lifecycle.WindowsServiceLifecycle
	-javaagent:"opentelemetry-javaagent.jar"
	-Dotel.resource.attributes=service.name=jenkins-service,service.namespace=JENKINS,service.code=JK1001
	-Dotel.metrics.export.interval=1000
	-Dotel.traces.exporter=otlp
	-Dotel.metrics.exporter=otlp
	-Dotel.logs.exporter=otlp
	-Dotel.service.name=spring-reporting-service
	-Dotel.exporter.otlp.endpoint=http://127.0.0.1:9999
	-Dotel.exporter.otlp.traces.endpoint=http://127.0.0.1:9999
	-Dotel.exporter.otlp.metrics.endpoint=http://127.0.0.1:9999
	-Dotel.exporter.otlp.logs.endpoint=http://127.0.0.1:9999
	-Dotel.exporter.otlp.protocol=grpc
	-jar "C:\Program Files\Jenkins\jenkins.war"
	--httpPort=7070
	--webroot="%ProgramData%\Jenkins\war"
	</arguments>
	=====================================================================


	# 2안 - 플러그인 설치(젠킨스에서 설치)
	https://plugins.jenkins.io/opentelemetry/
		1. Jenkins 관리 클릭
		2. 플러그인 관리 클릭
		3. 설치가능 에서 "OpenTelemetry" 검색
			Warning: This plugin is built for Jenkins 2.361.4 or newer. Jenkins will refuse to load this plugin if installed.
			※ 2.361.4 버전에서 작동한다고함...

	# 3안 - 플러그인 설치(수동 다운로드)
		※ 이거 좀 고려해봐야함, 필요한 플러그인들 버전이 죄다 2021년도에 나온 버전들이라서..
        ※ 안됨, 10번까지 싹다 했을 때 플러그인 종속 문제가 더 많아짐

		https://updates.jenkins.io/download/plugins/opentelemetry/
		https://updates.jenkins.io/download/plugins/opentelemetry/#2.4.0
		※최소 필요버전이 2.277.1 인 2.4.0 버전 다운로드
		
		1. 다운받은 opentelemetry.hpi 플러그인을 아래의 경로에 이동
			C:\ProgramData\Jenkins\.jenkins\plugins
		
		2. Jenkins 재시작
		
		3. Jenkins관리에서 확인
			=====================================================================
			Some plugins could not be loaded due to unsatisfied dependencies. Fix these issues and restart Jenkins to re-enable these plugins.

			Dependency errors:

			OpenTelemetry Plugin (2.4.0)
			Plugin is missing: workflow-job (2.41)
			Plugin is missing: workflow-basic-steps (2.22)
			Plugin is missing: pipeline-stage-step (2.5)
			Plugin is missing: workflow-cps (2.94)
			Plugin is missing: workflow-durable-task-step (2.40)
			Plugin is missing: pipeline-build-step (2.15)
			Plugin is missing: pipeline-model-definition (1.9.2)
			Plugin is missing: plain-credentials (1.7)
			Plugin is missing: okhttp-api (4.9.3-105.vb96869f8ac3a)
			Plugin is missing: workflow-multibranch (2.24)
			Plugin is missing: jackson2-api (2.13.0-230.v59243c64b0a5)
			Plugin is missing: credentials (2.6.1)
			=====================================================================
		
		4. 필요한 플러그인들이 없어서 실행이 안됨...... 위에 있는 모든 플러그인을 설치해야함..
			- 싹다 다운로드 하기로함
			
		5. 플러그인 찾기
			https://updates.jenkins-ci.org/download/plugins/
			https://updates.jenkins-ci.org/download/plugins/workflow-job#2.41
			https://updates.jenkins-ci.org/download/plugins/workflow-basic-steps#2.22
			https://updates.jenkins-ci.org/download/plugins/pipeline-stage-step#2.5
			https://updates.jenkins-ci.org/download/plugins/workflow-cps#2.94
			https://updates.jenkins-ci.org/download/plugins/workflow-durable-task-step#2.40
			https://updates.jenkins-ci.org/download/plugins/pipeline-build-step#2.15
			https://updates.jenkins-ci.org/download/plugins/pipeline-model-definition#1.9.2
			https://updates.jenkins-ci.org/download/plugins/plain-credentials#1.7
			https://updates.jenkins-ci.org/download/plugins/okhttp-api#4.9.3-105.vb96869f8ac3a
			https://updates.jenkins-ci.org/download/plugins/workflow-multibranch#2.24
			https://updates.jenkins-ci.org/download/plugins/jackson2-api#2.13.0-230.v59243c64b0a5
			https://updates.jenkins-ci.org/download/plugins/credentials#2.6.1
			https://updates.jenkins-ci.org/download/plugins/snakeyaml-api#1.29.1

		6. 위 플러그인들 다운로드 후 아래의 경로에 복사
			C:\ProgramData\Jenkins\.jenkins\plugins
		
		7. jenkins 재시작
		
		8. Jenkins 관리에서 플러그인들 모두 업데이트

		9. Jenkins 재시작

		10. 안됨 걍 답이없음


# Jenkins 오픈텔레메트리 설정
    ※ 플러그인 최신버전이면 될거같은데 불가능함
	https://docs.newrelic.com/kr/docs/infrastructure/other-infrastructure-integrations/monitoring-jenkins-ot/
