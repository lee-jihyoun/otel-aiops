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