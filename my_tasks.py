from functools import reduce

import tasks


def xrange(x):
    return iter(range(x))


@tasks.task(name='multiprint',
            json_schema={
                'type': 'object',
                'properties': {
                    'msg': {'type': 'string'},
                    'count': {'type': 'integer', 'minimum': 1}
                },
                'required': ['msg']
            })
def multi_print(msg, count=10):
    return '\n'.join(msg for _ in xrange(count))


class Multiply(tasks.BaseTask):
    name = 'mult'
    json_schema = {
        'type': 'object',
        'properties': {
            'operands': {
                'type': 'array',
                'minItems': 1,
                'items': {'type': 'number'}
            }
        }
    }

    def run(self, operands):
        return reduce(lambda x, y: x * y, operands)


if __name__ == '__main__':
    tasks.run_cli()
