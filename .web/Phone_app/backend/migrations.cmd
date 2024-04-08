@echo off
call .\venv\Scripts\activate
python.exe .\manage.py makemigrations 
python.exe .\manage.py migrate

