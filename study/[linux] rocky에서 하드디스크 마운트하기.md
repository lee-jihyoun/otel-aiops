## 250G의 SSD는 이미 마운트되었는데 7TB 하드디스크는 마운트되지 않은 상황.

# 하드디스크 UUID 검색 및 복사
ls -l /dev/disk/by-uuid

# 마운트를 위해 설정파일 열기
vi /etc/fstab

# 마운트할 위치의 디렉토리 생성
mkdir /mnt/data

# 디렉토리를 누구나 읽고 쓸 수 있게 권한 부여
chmod 777 /mnt/data
