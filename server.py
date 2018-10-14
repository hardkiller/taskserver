from flask import Flask,jsonify, json, render_template, send_from_directory, request
from flask_script import Manager
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate, MigrateCommand
from flask_mail import Mail, Message

import os
import re
import tasks
import multiprocessing
import datetime

from my_tasks import Multiply, multi_print


static_file_dir = os.path.join(os.path.dirname(os.path.realpath(__file__)), 'public')


app = Flask(__name__, template_folder='template')

app.config.from_pyfile('config.cfg')

mail = Mail(app)

db = SQLAlchemy(app)
migrate = Migrate(app, db)

manager = Manager(app)
manager.add_command('db', MigrateCommand)


class TaskResult(db.Model):
    __tablename__ = 'task_results'
    id = db.Column(db.Integer, primary_key=True)
    task_name = db.Column(db.String(255))
    start_datetime = db.Column(db.DateTime)
    end_datetime = db.Column(db.DateTime)
    parameters = db.Column(db.Text)
    email = db.Column(db.String(255))
    result = db.Column(db.Text)


@app.route('/')
def root():
    return send_from_directory(static_file_dir, 'index.html')


def validate_mail(email):

    if not email:
        return False

    if len(email) < 7:
        return False

    return re.match(r"[^@]+@[^@]+\.[^@]+", email)


def create_task(task_params):

    task_result = TaskResult()
    task_result.start_datetime = datetime.datetime.utcnow()
    task_result.end_datetime = None
    task_result.task_name = task_params.get("task_name")
    task_result.parameters = task_params.get("params")
    task_result.email = task_params.get("email")
    task_result.result = None

    db.session.add(task_result)
    db.session.commit()

    return task_result


def update_task_results(task_id, result):

    task_result = db.session.query(TaskResult).get(task_id)
    task_result.end_datetime = datetime.datetime.utcnow()
    task_result.result = result
    db.session.add(task_result)
    db.session.commit()


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

    task_object = None

    try:
        task_object = create_task(params)

    except Exception as error:

        result = {
            "status": "ERROR",
            "error_code": 102,
            "error_msg": "Ошибка записи задачи в базу: " + str(error)
        }
        send_end.send(result)
        return

    finally:
        print("Created resultTask entity with id %s" % task_object.id)

    try:
        parameters = json.loads(task_params)
        result_value = tasks.run(task_name, parameters)
        result = {"result": result_value}

        if task_object is not None and task_object.id is not None:
            update_task_results(task_object.id, result_value)

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


def serialize_task(task_obj):
    return {
        "id": task_obj.id,
        "start_datetime": task_obj.start_datetime,
        "end_datetime": task_obj.end_datetime,
        "task_name": task_obj.task_name,
        "parameters": task_obj.parameters,
        "result": task_obj.result
    }


@app.route("/tasks_list", methods=['GET'])
def tasks_list():

    task_items = TaskResult.query.all()
    return jsonify([(serialize_task(row)) for row in task_items])


@app.route("/get_task_workers", methods=['GET'])
def get_task_workers():
    task_workers = tasks.get_workers_list()
    return jsonify(task_workers)


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
