from flask import Flask, render_template, send_from_directory

import os

static_file_dir = os.path.join(os.path.dirname(os.path.realpath(__file__)), 'public')

app = Flask(__name__, template_folder='template')

app.config['STATIC_FOLDER'] = '/public'

@app.route('/')
def root():
    message = "Hello, World"
    return render_template('index.html', message=message)

@app.route('/<path:path>')
def static_proxy(path):

    if not os.path.isfile(os.path.join(static_file_dir, path)):
        path = os.path.join(path, 'index.html')

    return send_from_directory(static_file_dir, path)
