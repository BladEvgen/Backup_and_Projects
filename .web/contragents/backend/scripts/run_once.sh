#!/bin/bash
read -p "Enter database name: " db_name_from_terminal
read -p "Enter username: " db_user_from_terminal
read -s -p "Enter password: " db_password_from_terminal
echo

echo "db_host = "localhost"" > ../.env
echo "db_port = 5432" >> ../.env
echo "db_name = "$db_name_from_terminal"" >> ../.env
echo "db_user = "$db_user_from_terminal"" >> ../.env
echo "db_password = "$db_password_from_terminal"" >> ../.env
