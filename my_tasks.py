from functools import reduce

import tasks


def xrange(x):
    return iter(range(x + 1))


@tasks.task(name='multiprint')
def multi_print(msg, count=10):
    return '\n'.join(msg for _ in xrange(count))


class Multiply(tasks.BaseTask):
    name = 'mult'

    def run(self, operands):
       return reduce(lambda x, y: x*y, operands)


if __name__ == '__main__':
    tasks.run_cli()