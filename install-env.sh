#!/bin/bash

# rm -rf ./venv
# mkdir ./venv
# virtualenv ./venv
# ./venv/bin/activate


# required to install mysql client dev library
# apt-get install libmariadbclient-dev
# apt-get install python-dev
# apt install default-libmysqlclient-dev
# apt-get install python3-dev

# необходимые переменные окружения
export FLASK_APP=server.py

# обновляем сам пакетный менеджер
./venv/bin/pip install --upgrade pip

./venv/bin/pip install Flask

./venv/bin/pip install flask-sqlalchemy

./venv/bin/pip install flask-migrate

./venv/bin/pip install flask-script

./venv/bin/pip install configparser

./venv/bin/pip install mysqlclient

./venv/bin/pip install Flask-Mail
