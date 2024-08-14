#!/usr/bin/env python3
'''Implementing an expiring web cache and tracker'''
import redis
import requests
from functools import wraps
from typing import Callable


db_whs = redis.Redis()
'''implementing a get_page function'''


def cash_db(method: Callable) -> Callable:
    '''this func will get data cach'''
    @wraps(method)
    def cvr(url) -> str:
        '''this is coevering func.'''
        db_whs.incr(f'count:{url}')
        result = db_whs.get(f'result:{url}')
        if result:
            return result.decode('utf-8')
        result = method(url)
        db_whs.set(f'count:{url}', 0)
        db_whs.setex(f'result:{url}', 10, result)
        return result
    return cvr


@cash_db
def get_page(url: str) -> str:
    '''this func will ret page data'''
    return requests.get(url).text
