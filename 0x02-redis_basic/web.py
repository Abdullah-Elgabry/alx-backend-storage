#!/usr/bin/env python3
''' Implementing an expiring web cache and tracker...'''
import redis
import requests
from functools import wraps
from typing import Callable


redis_store = redis.Redis()


def data_cacher(method: Callable) -> Callable:
    '''This func will return the chash dta'''
    @wraps(method)
    def invoker(url) -> str:
        '''This func will return dta from db'''
        redis_store.incr(f'count:{url}')
        result = redis_store.get(f'result:{url}')
        if result:
            return result.decode('utf-8')
        result = method(url)
        redis_store.set(f'count:{url}', 0)
        redis_store.setex(f'result:{url}', 10, result)
        return result
    return invoker


@data_cacher
def get_page(url: str) -> str:
    '''This func will get the brev data'''
    return requests.get(url).text
