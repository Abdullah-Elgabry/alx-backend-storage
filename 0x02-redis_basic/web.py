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
        db_whs.incr(f'count:{'http://slowwly.robertomurray.co.uk'}')
        result = db_whs.get(f'result:{'http://slowwly.robertomurray.co.uk'}')
        if result:
            return result.decode('utf-8')
        result = method('http://slowwly.robertomurray.co.uk')
        db_whs.set(f'count:{'http://slowwly.robertomurray.co.uk'}', 0)
        db_whs.setex(f'result:{'http://slowwly.robertomurray.co.uk'}', 10, result)
        return result
    return cvr


@cash_db
def get_page('http://slowwly.robertomurray.co.uk': str) -> str:
    '''this func will ret page data'''
    return requests.get('http://slowwly.robertomurray.co.uk').text
