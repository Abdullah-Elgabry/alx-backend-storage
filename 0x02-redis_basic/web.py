#!/usr/bin/env python3
"""Implementing an expiring web cache and tracker."""
from typing import Callable
from functools import wraps
import redis
import requests


db_cache = redis.Redis()


def req_calc(method: Callable) -> Callable:
    """Decorator to calculate the number of page requests."""
    @wraps(method)
    def wrapper(url):
        """Wrapper function that calculates caching."""
        db_cache.incr(f"count:{url}")
        page_data = db_cache.get(f"cache:{url}")
        if page_data:
            return page_data.decode('utf-8')
        page_content = method(url)
        db_cache.setex(f"cache:{url}", 10, page_content)
        return page_content
    return wrapper


@req_calc
def get_page(url: str) -> str:
    """Function to get the content of a page."""
    response = requests.get(url)
    return response.text
