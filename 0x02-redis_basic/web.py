#!/usr/bin/env python3
''' Implementing an expiring web cache and tracker '''
from typing import Callable
from functools import wraps
import redis
import requests


db_cach = redis.Redis()


def req_calc(method: Callable) -> Callable:
    ''' this func will ret the page req num '''
    @wraps(method)
    def cvr(url):
        ''' covering func that calc the caching '''
        db_cach.incr(f"count:{url}")
        page_dta = db_cach.get(f"caching:{url}")
        if page_dta:
            return page_dta.decode('utf-8')
        pg_db = method(url)
        db_cach.setex(f"caching:{url}", 10, pg_db)
        return pg_db
    return cvr

@req_calc
def get_page(url: str) -> str:
    ''' this func will reet the page req '''
    req = requests.get(url)
    return req.text
