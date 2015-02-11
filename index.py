import os
import sys
import requests
import argparse
import redis
import rq

def count_words_at_url(url):
    resp = requests.get(url)
    return len(resp.text.split())


host = 'localhost'
actions = {'count': count_words_at_url}


def get_args():
    parser = argparse.ArgumentParser(description='Sling URLs through or RQ demo')
    parser.add_argument('action', type=str, choices=actions.keys(), help="Worker action to perform")

    parser.add_argument('url', type=str, help='Url to act on')
    parser.add_argument('-s', '--server', const=host, action='store_const',
                        help='Redis hostname to connect to')

    return parser.parse_args()


def main():
    args = get_args()
    conn = redis.Redis(host=host)
    worker = rq.Queue(connection=conn)
    result = worker.enqueue(actions.get(args.action), args.url)

    print result


if __name__ == '__main__':
    main()
