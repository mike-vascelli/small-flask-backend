from abc import ABC, abstractmethod
from typing import Any


class Cache(ABC):
    @abstractmethod
    def insert(self, key: str, value: Any) -> None:
        pass

    @abstractmethod
    def get(self, key: str) -> Any:
        pass

    @abstractmethod
    def remove(self, key: str) -> None:
        pass
