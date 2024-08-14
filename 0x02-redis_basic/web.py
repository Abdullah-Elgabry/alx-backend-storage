#!/usr/bin/env python3
''' Implementing an expiring web cache and tracker '''

from functools import wraps
import requests
from typing import Callable
import redis

db_wrhs = redis.Redis()


def count_requests(method: Callable) -> Callable:
    ''' this func will get the cash from db  '''
    @wraps(method)
    def wrapper(url):
        ''' covering func '''
        db_wrhs.incr(f"count:{url}")
        db_cach = db_wrhs.get(f"cached:{url}")
        if db_cach:
            return db_cach.decode('utf-8')
        html = method(url)
        db_wrhs.setex(f"cached:{url}", 10, html)
        return html

    return wrapper


@count_requests
def get_page(url: str) -> str:
    ''' this will return the page req '''
    req = requests.get(url)
    return req.text
