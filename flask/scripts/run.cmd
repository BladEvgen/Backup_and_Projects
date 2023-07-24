@echo off

set "MY_CODE_PATH=D:\.CODE\PY\FLASK"


call "%MY_CODE_PATH%\env\Scripts\activate"

flask --app main run --debug --port=8000 --host=127.0.0.1


pause
