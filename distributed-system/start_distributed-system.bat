@echo off
start cmd /k "cd ./board-system && start_board_system.bat"
start cmd /k "cd ./ldap-system && start_ldap_system.bat"
start cmd /k "cd ./log-system && start_log_system.bat"
start cmd /k "cd ./user-system && start_user_system.bat"