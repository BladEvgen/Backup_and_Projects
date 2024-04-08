@echo off
set /p db_name_from_terminal="Enter database name: "
set /p db_user_from_terminal="Enter username: "
set /p db_password_from_terminal="Enter password: "

echo db_host = "localhost" > ..\.env
echo db_port = 5432 >> ..\.env
echo db_name = "%db_name_from_terminal%" >> ..\.env
echo db_user = "%db_user_from_terminal%" >> ..\.env
echo db_password = "%db_password_from_terminal%" >> ..\.env
