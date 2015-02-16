import sys
import lxml.html
import requests
import hashlib
from furl import furl
from elasticsearch import Elasticsearch
from lxml.cssselect import CSSSelector
from rq import use_connection, Queue


def get_queue():
    use_connection()
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
    print results
    return results


def make_img_url(url, path):
    u = furl(url)
    u.path = path
    as_string = "%s" % (u)
    print as_string
    return as_string


def get_img(url, href):
    r = requests.get(href)
    r.raise_for_status()
    job = get_queue().enqueue(hash_img, url, href, r.content)
    print job
    return job.id


def hash_img(url, href, data):
    job = get_queue().enqueue(index_img, url, href, hashlib.sha1(data).hexdigest())
    print job
    return job.id


def index_img(url, href, hash):
    return {"url": url, "href": href, "hash": hash}
    es = Elasticsearch()
    return es.index(
        index='img-index',
        doc_type='indexed_image',
        body={"url": url, "href": href, "hash": hash}
    )

