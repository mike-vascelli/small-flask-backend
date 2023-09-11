from typing import List

from caches.algorithms_cache import use_algorithms_cache, clear_algorithms_cache
from models.algorithm import Algorithm
from models.model import Model
from repositories.repository import Repository


class AlgorithmsService:
    def __init__(self, repository: Repository):
        self.repository = repository

    @clear_algorithms_cache
    def create(self, **kwargs) -> Model:
        algorithm = Algorithm(**kwargs)
        return self.repository.create(algorithm)

    @clear_algorithms_cache
    def update(self, pk: str, **kwargs) -> None:
        algorithm = self.repository.retrieve_by_pk(pk)
        updated_algorithm = algorithm.update_with(kwargs)
        self.repository.update(updated_algorithm)

    @use_algorithms_cache
    def retrieve_all(self) -> List[Model]:
        return self.repository.retrieve_all()
