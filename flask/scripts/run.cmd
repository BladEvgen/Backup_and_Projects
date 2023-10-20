@echo off

set "MY_CODE_PATH=D:\Step_Code\Home_Works\new\flask"


call "%MY_CODE_PATH%\env\Scripts\activate"

pip freeze > requirements.txt

flask --app main run --debug --port=8000 --host=127.0.0.1


pause
