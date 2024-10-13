# nginx설치
dnf install nginx

# nginx 로그 디렉토리 권한 변경
chown -R nginx:nginx /var/log/nginx

# 기동 확인
systemctl start nginx
systemctl enable nginx

# 방화벽 추가
firewall-cmd --permanent --add-service=http
firewall-cmd --reload

# 배포 폴더 추가
mkdir /opt/www

# 배포 폴더 권한 변경
chown -R nginx:nginx /opt/www

# nginx 설정 백업
cp /etc/nginx/nginx.conf /etc/nginx/nginx.conf_backup_2024.10.13

# nginx 설정 변경 (배포 디렉토리 변경)
vi /etc/nginx/nginx.conf
=====================================================================
        #root         /usr/share/nginx/html;
        root            /opt/www;
=====================================================================

# nginx config파일 문법 검사
nginx -t

# nginx 재시작
systemctl restart nginx

# 배포할 내용 복사
cp -r /opt/dsquare-frontend/webview/dist/* /opt/www/
※ dist에 있는 내용들을 그대로 www 폴더 밑으로 복사

# 권한 변경
chown -R nginx:nginx /opt/www

# nginx 재시작
systemctl restart nginx

---
Springboot연동

# nginx에서 Springboot 설정
vi /etc/nginx/nginx.conf
=====================================================================
location /api/ {
proxy_pass http://localhost:8090/;
proxy_set_header Host $host;
proxy_set_header X-Real-IP $remote_addr;
proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
proxy_set_header X-Forwarded-Proto $scheme;
}
=====================================================================

# 로그 확인
tail -f /var/log/nginx/access.log

#  오류메시지
tail -f /var/log/nginx/error.log

2024/10/13 21:50:46 [crit] 2030642#0: *4 connect() to [::1]:8090 failed (13: Permission denied) while connecting to upstream, client: 100.114.155.127, server: _, request: "POST /api/login HTTP/1.1", upstream: "http://[::1]:8090/login", host: "100.83.227.59"
2024/10/13 21:50:46 [crit] 2030642#0: *4 connect() to 127.0.0.1:8090 failed (13: Permission denied) while connecting to upstream, client: 100.114.155.127, server: _, request: "POST /api/login HTTP/1.1", upstream: "http://127.0.0.1:8090/login", host: "100.83.227.59"



# 8090 포트로 서비스가 실행중인지 확인
	[root@localhost nginx]# lsof -i :8090
	COMMAND     PID USER   FD   TYPE    DEVICE SIZE/OFF NODE NAME
	java    2015329 root   19u  IPv6 405557842      0t0  TCP *:opsmessaging (LISTEN)

# SELinux 사용중인지 확인
	getenforce
	-> Enforcing
	※ Enforcing는 사용중임

# SELinux 포트 접근 차단 설정 확인
getsebool httpd_can_network_connect
-> httpd_can_network_connect --> off

# SELinux가 NGINX의 포트 접근 차단 해제
setsebool -P httpd_can_network_connect on


# SELinux 포트 접근 차단 설정 확인
getsebool httpd_can_network_connect
-> httpd_can_network_connect --> on

# nginx 재시작
systemctl restart nginx


