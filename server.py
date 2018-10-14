from flask import Flask,jsonify, json, render_template, send_from_directory, request
from flask_script import Manager
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate, MigrateCommand
from flask_mail import Mail, Message

import os
import re
import tasks
import multiprocessing

from my_tasks import Multiply, multi_print


static_file_dir = os.path.join(os.path.dirname(os.path.realpath(__file__)), 'public')

app = Flask(__name__, template_folder='template')

app.config.from_pyfile('config.cfg')

mail = Mail(app)

db = SQLAlchemy(app)
migrate = Migrate(app, db)

manager = Manager(app)
manager.add_command('db', MigrateCommand)


class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(128))


@app.route('/')
def root():
    message = "Hello, World"
    return render_template('index.html', message=message)


def validate_mail(email):

    if not email:
        return False

    if len(email) < 7:
        return False

    return re.match(r"[^@]+@[^@]+\.[^@]+", email)


def send_result_to_mail(email, result):

    if email is None or len(email) < 7:
        return

    subject = "Результаты выполнения задачи"
    body = "Пустой ответ"

    if result is not None:
        if result.get("status") == "ERROR":
            body = result.get("error_msg")
        else:
            body = result.get("result")

    recipients = [email]

    msg = Message(subject=subject, body=body, recipients=recipients)

    with app.open_resource("config.cfg.example") as fp:
        msg.attach("config.cfg.example", "text/plain", fp.read())

    mail.send(msg)
    return


def task_worker(params, send_end):

    task_name = params.get('task_name')
    task_params = params.get('params')
    email = params.get('email')

    try:
        parameters = json.loads(task_params)
        result_value = tasks.run(task_name, parameters)
        result = {"result": result_value}

    except Exception as error:

        result = {
            "status": "ERROR",
            "error_code": 100,
            "error_msg": "Ошибка выполнения задачи: " + str(error)
        }

    finally:

        if email is not None and len(email) > 7:
            send_result_to_mail(email, result)

        send_end.send(result)


@app.route("/run_task", methods=['POST'])
def run_task():

    data = json.loads(request.data)
    email = data.get('email')

    if email is not None and len(email) > 0 and not validate_mail(email):

        result = {
            "status": "ERROR",
            "error_code": 101,
            "error_msg": "указан некорректный почтовый ящик %s" % email
        }
        return jsonify(result)

    thread_params = {
        "params": data.get('params'),
        "task_name": data.get('task_name'),
        "email": email
    }

    recv_end, send_end = multiprocessing.Pipe(False)

    p = multiprocessing.Process(
        target=task_worker,
        args=(thread_params, send_end)
    )
    p.start()

    if email is not None and len(email) > 0:
        result = {"status": "OK"}
        return jsonify(result)

    result = recv_end.recv()

    return jsonify(result)


@app.route('/<path:path>')
def static_proxy(path):
    if not os.path.isfile(os.path.join(static_file_dir, path)):
        path = os.path.join(path, 'index.html')

    return send_from_directory(static_file_dir, path)


if __name__ == '__main__':
    manager.run()
