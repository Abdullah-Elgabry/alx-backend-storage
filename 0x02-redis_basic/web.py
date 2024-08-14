#!/usr/bin/env python3
''' Implementing an expiring web cache and tracker '''

from functools import wraps
import redis
import requests
from typing import Callable

redis_ = redis.Redis()


def count_requests(method: Callable) -> Callable:
    ''' this func will ret the page req num '''
    @wraps(method)
    def wrapper(url):
        ''' covering func '''
        redis_.incr(f"count:{url}")
        cached_html = redis_.get(f"cached:{url}")
        if cached_html:
            return cached_html.decode('utf-8')
        html = method(url)
        redis_.setex(f"cached:{url}", 10, html)
        return html

    return wrapper


@count_requests
def get_page(url: str) -> str:
    ''' this func will reet the page req '''
    req = requests.get(url)
    return req.text
