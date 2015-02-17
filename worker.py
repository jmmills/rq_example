import requests
import lxml.html

from redis import Redis
from rq import use_connection, Queue

from hashlib import sha1
from furl import furl
from elasticsearch import Elasticsearch
from lxml.cssselect import CSSSelector


def get_queue():
    use_connection(Redis(host='redis'))
    return Queue()


def echo(stuff):
    return stuff


def count_text(text):
    return {'data': len(text.split())}


def count_words_at_url(url):
    r = requests.get(url)
    job = get_queue().enqueue(count_text, r.text)
    return job.id


def index(url):
    return get_html(url)


def get_html(url):
    r = requests.get(url)
    r.raise_for_status()
    job = get_queue().enqueue(sel_img, url, r.text)
    return job.id


def sel_img(url, html):
    tree = lxml.html.fromstring(html)
    sel = CSSSelector('img')
    q = get_queue()
    results = [q.enqueue(get_img, url, make_img_url(url, m.get('src'))) for m in sel(tree)]
    return results


def make_img_url(url, path):
    u = furl(url)
    u.path = path
    as_string = "%s" % (u)
    return as_string


def get_img(url, href):
    r = requests.get(href)

    if r.status_code == 200:
        job = get_queue().enqueue(hash_img, url, href, r.content)
    else:
        job = get_queue().enqueue(index_img_error, url, href, r)

    return job.id


def index_img_error(url, href, r):
    return send_to_es(url, href, {
        'status': r.status_code,
        'reason': r.reason
    })


def hash_img(url, href, data):
    job = get_queue().enqueue(index_img, url, href, sha1(data).hexdigest())
    return job.id


def index_img(url, href, hash):
    return send_to_es(url, href, {"url": url, "href": href, "hash": hash})


def send_to_es(url, href, data):
    es = Elasticsearch('http://elasticsearch:9200')
    return es.index(
        index='img-index',
        doc_type='indexed_image',
        body={"url": url, "href": href, "hash": data}
    )


