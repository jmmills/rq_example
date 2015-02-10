from redis import Redis
from rq import Queue

import requests


def count_words_at_url(url):
    resp = requests.get(url)
    return len(resp.text.split())


q = Queue(connection=)

