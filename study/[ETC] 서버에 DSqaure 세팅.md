## DSquare frnotend 세팅
# git clone
    cd /opt
    git clone https://github.com/100yeony/dsquare-frontend.git
    git checkout dev

# 서버에 노드 16버전 설치
    dnf remove nodejs
    dnf install -y gcc-c++ make
    curl -sL https://rpm.nodesource.com/setup_16.x | sudo bash -
    dnf install -y nodejs

# dsquare-frontend 의존성 라이브러리 설치
    cd webview
    npm install

# vuetify 설치
    npm install vuetify@next

# 버전 안맞아서 오류나면 sass 설치
    npm uninstall node-sass
    npm install sass

# 실행
    npm run serve

# build하기
    npm run build

# 빌드 파일 실행
    npx serve -s build



## DSquare backend 세팅
# git clone
    cd /opt
    git clone https://github.com/100yeony/dsquare-backend.git
    git checkout develop

# 권한 부여(git pull 받을때마다 아래 명령어와 jar 파일 빌드 새로 해야함)
    cd /opt
    chmod -R 777 dsquare-backend/

# jar 파일 빌드(오래걸림 55분)
    cd dsquare-backend/
    ./gradlew assemble

# jar 파일 실행
    cd /opt/dsquare-backend/build/libs
    JASYPT_ENCRYPTOR_PASSWORD=ktds.dsquare java -jar DSquare-User-0.0.1-SNAPSHOT.jar

# 백그라운드로 실행
	JASYPT_ENCRYPTOR_PASSWORD=ktds.dsquare nohup java -jar DSquare-User-0.0.1-SNAPSHOT.jar > output.log 2>&1 &

