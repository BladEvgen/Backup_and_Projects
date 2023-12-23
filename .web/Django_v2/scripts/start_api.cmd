py -3.11 -m venv sanic_env

call sanic_env\scripts\activate
pip install sanic_requirements.txt
pip freeze > sanic_requirements.txt

cd sanic\

python main.py 