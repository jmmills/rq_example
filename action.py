import os
import sys
import requests
import argparse
import redis
from worker import count_words_at_url, index
from rq_scheduler import Scheduler
from rq import use_connection, Queue
from rq.job import Job
from datetime import datetime


def wait_for_job(job_id, conn):
    job = Job().fetch(job_id, conn)

    print type(job.result)

    while job.result is None:
        print "Waiting for job %s results" % (job.id)

    if type(job.result) is not dict:
        return wait_for_job(job.result, conn)
    else:
        return job.result


actions = {'count': count_words_at_url, 'index': index}


def get_args():
    parser = argparse.ArgumentParser(description='Sling URLs through or RQ demo')
    parser.add_argument('action', type=str, choices=actions.keys(), help="Worker action to perform")

    parser.add_argument('url', type=str, help='Url to act on')
    parser.add_argument('-s', '--server', action='store', dest='server',
                        help='Redis hostname to connect to')

    return parser.parse_args()


def main():
    args = get_args()
    conn = redis.Redis(host=args.server)

    use_connection(conn)

    worker = Queue()

    print "Running %s from %s redis" % (args.action, args.server)

    if args.action == 'index':
        scheduler = Scheduler(connection=conn)
        print scheduler.schedule(
            scheduled_time=datetime.now(),
            func=actions.get(args.action),
            args=[args.url],
            interval=60,
            repeat=None
        )
    else:
        job = worker.enqueue(actions.get(args.action), args.url)
        print wait_for_job(job.id, conn)


if __name__ == '__main__':
    main()
