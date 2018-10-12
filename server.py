from flask import Flask, render_template, send_from_directory

from flask_script import Manager

from flask_sqlalchemy import SQLAlchemy

from flask_migrate import Migrate, MigrateCommand

import os

static_file_dir = os.path.join(os.path.dirname(os.path.realpath(__file__)), 'public')

app = Flask(__name__, template_folder='template')

app.config.from_pyfile('config.cfg')

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

@app.route('/<path:path>')
def static_proxy(path):

    if not os.path.isfile(os.path.join(static_file_dir, path)):
        path = os.path.join(path, 'index.html')

    return send_from_directory(static_file_dir, path)

if __name__ == '__main__':
    manager.run()