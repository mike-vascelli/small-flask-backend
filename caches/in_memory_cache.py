from typing import Any

from caches.cache import Cache


class InMemoryCache(Cache):
    def __init__(self):
        self.data = {}

    def insert(self, key: str, value: Any) -> None:
        self.data[key] = value

    def get(self, key: str) -> Any:
        return self.data.get(key)

    def remove(self, key: str) -> None:
        self.data.pop(key, None)
