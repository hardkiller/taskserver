#!/bin/bash

echo "mult"
./venv/bin/python ./my_tasks.py mult --params '{"operands": [3, 2, 8]}'

echo "multiprint"
./venv/bin/python ./my_tasks.py multiprint --params '{"msg": "hello", "count": 3}'


# schema tests

# echo "mult with schema errors"
# ./venv/bin/python ./my_tasks.py mult --params '{"operands": []}'

# echo "multiprint with schema errors"
#./venv/bin/python ./my_tasks.py multiprint --params '{"mesg": "hello", "count": 0}'