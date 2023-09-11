import dataclasses
import uuid
from typing import Dict

from models.model import Model


@dataclasses.dataclass
class Algorithm(Model):
    pk: uuid.UUID
    progress: float = 0

    def to_dict(self) -> Dict:
        return dataclasses.asdict(self)

    @classmethod
    def from_dict(cls, d) -> Model:
        return cls(**d)

    def clone(self) -> Model:
        return self.from_dict(self.to_dict())

    def update_with(self, data: Dict) -> Model:
        updated_dict = self.to_dict() | data
        return self.from_dict(updated_dict)
