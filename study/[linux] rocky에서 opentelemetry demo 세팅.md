## git 설치
    dnf install -y git

## git clone
    git clone https://github.com/open-telemetry/opentelemetry-demo.git

    cd opentelemetry-demo

## start demo
    [root@localhost opentelemetry-demo]# docker compose up --force-recreate --remove-orphans --detach
    =================
    [+] Running 14/24
    ⠴ grafana [⠀⠀⠀⠀⠀⠀⠀⠀⠀] Pulling                                                                                                                  56.6s 
    ⠴ recommendationservice [⠀⠀⠀⠀⠀] Pulling                                                                                                        56.6s 
    ⠴ loadgenerator [⠀⠀⠀⠀⠀⠀⠀⠀⠀] Pulling                                                                                                            56.6s 
    ⠴ accountingservice [⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀] Pulling      
    =================