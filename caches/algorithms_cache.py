import functools

from flask import current_app

from caches.in_memory_cache import InMemoryCache

in_memory_cache = InMemoryCache()

cache_key = "algorithms"


def use_algorithms_cache(func):
    @functools.wraps(func)
    def inner(*args, **kwargs):
        result = in_memory_cache.get(cache_key)
        if result is not None:
            current_app.logger.debug("Reading algorithms from cache")
            return result
        current_app.logger.debug("Reading algorithms from DB")
        result = func(*args, **kwargs)
        in_memory_cache.insert(cache_key, result)
        return result

    return inner


def clear_algorithms_cache(func):
    @functools.wraps(func)
    def inner(*args, **kwargs):
        result = func(*args, **kwargs)
        in_memory_cache.remove(cache_key)
        return result

    return inner
