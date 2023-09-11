from abc import ABC, abstractmethod
from typing import Dict, Any


class Model(ABC):
    EXPECTED_PRIMARY_KEY_NAMES = ("pk", "id")

    def get_pk(self) -> Any:
        for name in self.EXPECTED_PRIMARY_KEY_NAMES:
            pk = getattr(self, name, None)
            if pk:
                return pk

        raise UnknownPrimaryKeyName(
            f"{self.__class__.__name__} has no valid primary key name."
            f" The allowed names are: {self.EXPECTED_PRIMARY_KEY_NAMES}"
        )

    @abstractmethod
    def update_with(self, data: Dict) -> "Model":
        pass

    @abstractmethod
    def to_dict(self) -> Dict:
        pass

    @abstractmethod
    def clone(self) -> "Model":
        pass


class UnknownPrimaryKeyName(Exception):
    def __init__(self, message):
        super().__init__()
        self.message = message
