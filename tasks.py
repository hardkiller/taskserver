# -*- coding: utf-8 -*-

import sys
import inspect
import json
from jsonschema import validate


class BaseTask:
    name = "test"
    json_schema = None
    task_runner = True

    def __init__(self):
        return None

    def run(self, arg):
        return None


def task(name, json_schema):
    def runfunc(method):
        def wrap(args):
            return method(**args)
        wrap.name = name
        wrap.json_schema = json_schema
        wrap.task_runner = True
        return wrap
    return runfunc


def get_task_runner(task_name):
    for name, obj in inspect.getmembers(sys.modules['__main__']):

        if hasattr(obj, 'task_runner') and hasattr(obj, 'name') and obj.name == task_name:
            return obj
    return None


def validate_parameters(json_schema, parameters):
    return validate(parameters, json_schema)


def run(task_name, parameters):

    runner = get_task_runner(task_name)

    if runner is None:
        error = 'Не найден исполнитель задачи с указанным именем %s' % task_name
        raise Exception(error)
        return None

    if not hasattr(runner, 'json_schema'):
        error = 'Указанный исполнитель задачи %s не содержит схемы валидации' % task_name
        raise Exception(error)
        return None

    json_schema = runner.json_schema
    print("JSON SCHEMA", json_schema)

    try:
        print("VALIDATE", parameters)
        validate_parameters(json_schema, parameters)
    except Exception:
        error = "Ошибка валидации схемы данных"
        raise Exception(error)

    if inspect.isclass(runner):
        task_object = runner()
        return task_object.run(**parameters)
    else:
        return runner(parameters)


def run_cli():

    if (len(sys.argv) != 4):
        print("usage: %s  <taskname> --params parameters " % (sys.argv[0]))
        return

    taskname = sys.argv[1]

    parameters = json.loads(sys.argv[3])

    result = run(taskname, parameters)

    print("TASK RESULTS", result)
