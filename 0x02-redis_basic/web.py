#!/usr/bin/env python3
''' Implementing an expiring web cache and tracker '''
from typing import Callable
from functools import wraps
import redis
import requests


db_cach = redis.Redis()


def count_requests(method: Callable) -> Callable:
    ''' this func will ret the page req num '''
    @wraps(method)
    def cvr(url):
        ''' covering func '''
        db_cach.incr(f"count:{url}")
        page_dta = db_cach.get(f"cached:{url}")
        if page_dta:
            return page_dta.decode('utf-8')
        html = method(url)
        db_cach.setex(f"cached:{url}", 10, html)
        return html
    return cvr


@count_requests
def get_page(url: str) -> str:
    ''' this func will reet the page req '''
    req = requests.get(url)
    return req.text
