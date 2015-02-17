import sys

sys.path.append('.')

from datetime import datetime
from redis import Redis
from rq_scheduler import Scheduler
from rq import Queue
from rq.job import Job, cancel_job
from shovel import task

import worker


def wait_for_job_to_finish(job):
    while job.result is None:
        pass

    return job.result


def send_job(redis, func, i):
    conn = Redis(host=redis)
    q = Queue(connection=conn)
    return q.enqueue(func, i)


def schedule_job(redis, func, interval, i):
    conn = Redis(host=redis)
    scheduler = Scheduler(connection=conn)
    return scheduler.schedule(
        scheduled_time=datetime.now(),
        func=func,
        args=[i],
        interval=interval,
        repeat=None
    )


def unschedule_job(redis, job_id):
    conn = Redis(host=redis)
    scheduler = Scheduler(connection=conn)
    job = Job.fetch(job_id)
    return scheduler.cancel(job)


@task
def count(url=None, redis='redis'):
    """Count the words at a url"""

    print wait_for_job_to_finish(send_job(redis, worker.count_words_at_url, url))


@task
def echo(data=None, redis='redis'):
    """Echo back data"""
    print wait_for_job_to_finish(send_job(redis, worker.echo, data))


@task
def index(on=None, redis='redis', interval=10):
    """Add url into image indexer"""
    print schedule_job(redis, worker.index, interval, on)


@task
def noindex(job_id=None, redis='redis'):
    """Add url into image indexer"""
    print unschedule_job(redis, job_id)


@task
def cancel(job_id=None, redis='redis'):
    """Cancel a job"""
    conn = Redis(host=redis)
    return cancel_job(job_id, conn)


@task
def date(redis='redis'):
    """Get date string from worker cluster"""
    print wait_for_job_to_finish(send_job(redis, worker.date, None))



