import sys

sys.path.append('.')

from datetime import datetime
from redis import Redis
from rq_scheduler import Scheduler
from rq import Queue
from shovel import task
from worker import count_words_at_url, echo, index


@task
def add(do='count',  redis='redis', with_input=None):
    '''Add an action into the worker queue'''

    conn = Redis(host=redis)

    def queue_it(func, i):
        q = Queue(connection=conn)
        return q.enqueue(func, i)

    def arg_count(x):
        return queue_it(count_words_at_url, x)

    def arg_echo(x):
        return queue_it(echo, x)

    def arg_index(x):
        scheduler = Scheduler(connection=conn)
        return scheduler.schedule(
            scheduled_time=datetime.now(),
            func=index,
            args=[x],
            interval=10,
            repeat=None
        )

    go = {
        'count': arg_count,
        'echo': arg_echo,
        'index': arg_index
    }

    print go[do](with_input).id



