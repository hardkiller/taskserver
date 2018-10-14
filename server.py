from flask import Flask,jsonify, json, render_template, send_from_directory, request
from flask_script import Manager
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate, MigrateCommand
from flask_mail import Mail, Message

import os
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


@app.route("/mail")
def mail_report():
    subject = "test sending mail with default sender"
    body = "Default sender qwe. Hello Flask message sent from Flask-Mail"
    recipients = ["any.default.receiver@gmail.com"]

    msg = Message(subject=subject, body=body, recipients=recipients)

    with app.open_resource("config.cfg.example") as fp:
        msg.attach("config.cfg.example", "text/plain", fp.read())

    mail.send(msg)
    return "Тестовое сообщение отправлено"


def task_worker(params, send_end):

    task_name = params.get('task_name')
    task_params = params.get('params')

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
        send_end.send(result)


@app.route("/run_task", methods=['POST'])
def run_task():

    data = json.loads(request.data)
    email = data.get('email')

    thread_params = {
         "params": data.get('params'),
         "task_name": data.get('task_name')
    }

    recv_end, send_end = multiprocessing.Pipe(False)

    p = multiprocessing.Process(
        target=task_worker,
        args=(thread_params, send_end)
    )
    p.start()

    if email is not None:
         print("we can send mail to %s" % email)

    result = recv_end.recv()

    return jsonify(result)


@app.route('/<path:path>')
def static_proxy(path):
    if not os.path.isfile(os.path.join(static_file_dir, path)):
        path = os.path.join(path, 'index.html')

    return send_from_directory(static_file_dir, path)


if __name__ == '__main__':
    manager.run()
