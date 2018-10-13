# -*- coding: utf-8 -*-

import sys
import inspect
import json


class BaseTask:
    def __init__(self):
        self.name = "test"

    def run(self, arg):
        return None


def task(name):
    def runfunc(method):
        def wrap(args):
            return method(**args)
        wrap.name = name
        return wrap
    return runfunc


def run(taskname, parameters):
    for name, obj in inspect.getmembers(sys.modules['__main__']):

        if hasattr(obj, 'name') and obj.name == taskname:

            if inspect.isclass(obj):
                taskobject = obj()
                return taskobject.run(**parameters)
            else:
                return obj(parameters)

    return None


def run_cli():

    if (len(sys.argv) != 4):
        print("usage: %s  <taskname> --params parameters " % (sys.argv[0]))
        return

    taskname = sys.argv[1]

    parameters = json.loads(sys.argv[3])

    result = run(taskname, parameters)

    print("TASK RESULTS", result)
