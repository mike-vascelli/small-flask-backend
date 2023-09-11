from abc import ABC, abstractmethod
from typing import List

from models.model import Model


class Repository(ABC):
    @abstractmethod
    def create(self, record: Model) -> Model:
        pass

    @abstractmethod
    def update(self, record: Model) -> None:
        pass

    @abstractmethod
    def retrieve_by_pk(self, pk) -> Model:
        pass

    @abstractmethod
    def retrieve_all(self) -> List[Model]:
        pass


class RepositoryClientError(Exception):
    def __init__(self, message):
        super().__init__()
        self.message = message


class UnprocessableRepositoryOperation(RepositoryClientError):
    def __init__(self, message):
        super().__init__(f"Missing or invalid record: {message}")


class RecordPKAlreadyExists(RepositoryClientError):
    def __init__(self, message):
        super().__init__(f"Duplicate primary key error: {message}")


class RecordNotFound(RepositoryClientError):
    def __init__(self, message):
        super().__init__(f"Record not found: {message}")
