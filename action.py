import os
import sys
import requests
import argparse
import redis
from worker import count_words_at_url, index
from rq import use_connection, Queue
from rq.job import Job


def wait_for_job(job_id):
    job = Job().fetch(job_id)

    while job.result is None:
        pass

    if type(job.result) is int:
        wait_for_job(job.result)
    else:
        return job.result


host = 'redis'
actions = { 'count': wait_for_count, 'index': index }


def get_args():
    parser = argparse.ArgumentParser(description='Sling URLs through or RQ demo')
    parser.add_argument('action', type=str, choices=actions.keys(), help="Worker action to perform")

    parser.add_argument('url', type=str, help='Url to act on')
    parser.add_argument('-s', '--server', const=host, action='store_const',
                        help='Redis hostname to connect to')

    return parser.parse_args()


def main():
    args = get_args()
    conn = redis.Redis()

    use_connection(conn)

    worker = Queue()

    print "Running %s" % (args.action)

    job = worker.enqueue(actions.get(args.action), args.url)

    print wait_for_job(job.id)


if __name__ == '__main__':
    main()
