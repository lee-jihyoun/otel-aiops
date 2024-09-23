# EPEL (Extra Packages for Enterprise Linux) 리포지토리 설치
	dnf install epel-release

# Redis 설치
	dnf install redis

# Redis 서비스 활성화 및 시작
	systemctl enable redis
	systemctl start redis

# Redis 서비스 상태 확인
	systemctl status redis

# Redis 설정 변경
	※ bind 가 여러개 있을수 있음, bind 0.0.0.0 만있으면되니 중복되는건 제거
	vi /etc/redis.conf
	=====================================================================
	bind 0.0.0.0	# 모든 IP 접속 허용

	port 16379		# 포트번호 변경

	requirepass 사용할비번	# 비밀번호

	protected-mode no		# 외부 접속 허용, 기본 yes
	=====================================================================




# Redis 재시작
	systemctl restart redis

# 방화벽 설정
	firewall-cmd --permanent --zone=public --add-port=16379/tcp
	firewall-cmd --reload

# 방화벽 설정 확인
	firewall-cmd --list-all