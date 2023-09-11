from typing import List

from models.model import Model
from repositories.repository import Repository, RecordPKAlreadyExists, RecordNotFound, UnprocessableRepositoryOperation


class InMemoryRepository(Repository):
    def __init__(self):
        self.data = {}

    def create(self, record: Model) -> Model:
        pk = record and record.get_pk()
        if pk is None:
            raise UnprocessableRepositoryOperation(record)
        if pk in self.data:
            raise RecordPKAlreadyExists(pk)
        self.data[pk] = record
        return self.data[pk]

    def update(self, record: Model) -> None:
        pk = record and record.get_pk()
        if pk is None:
            raise UnprocessableRepositoryOperation(record)
        if pk not in self.data:
            raise RecordNotFound(pk)
        self.data[pk] = record

    def retrieve_by_pk(self, pk) -> Model:
        """
        Returning a defensive copy of the record to prevent any reference modifications
        """
        record = pk is not None and self.data.get(pk)
        if not record:
            raise RecordNotFound(pk)
        return record.clone()

    def retrieve_all(self) -> List[Model]:
        """
        Returning a defensive copy of the records to prevent any reference modifications
        """
        return list(r.clone() for r in self.data.values())
