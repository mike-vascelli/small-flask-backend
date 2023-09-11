import dataclasses
import json
from abc import abstractmethod, ABC
from json import JSONDecodeError
from typing import Dict, List, Optional, Any, Callable


@dataclasses.dataclass
class Constraint:
    func: Callable[[any], bool]
    message: str


class Request(ABC):

    def __init__(self, request_data, **kwargs):
        self.is_validated = False
        self.errors = []
        self.valid_data = {}
        self.request_data = request_data
        self.kwargs = kwargs

    @abstractmethod
    def expected_fields(self) -> Dict[str, Any]:
        pass

    @abstractmethod
    def fields_constraints(self) -> Dict[str, Constraint]:
        pass

    def is_valid(self):
        if self.is_validated:
            return not self.errors

        parsed_json = self._deserialize()
        if not self.errors:
            self.valid_data = self._validate_fields(parsed_json)

        self.is_validated = True
        return not self.errors

    def error_details(self) -> List[Dict]:
        if not self.is_validated:
            raise NotValidated()
        return self.errors

    def validated_data(self) -> Dict:
        if not self.is_validated:
            raise NotValidated()
        return self.valid_data

    def _deserialize(self) -> Optional[Dict]:
        try:
            request_body = json.loads(self.request_data)
            return request_body | self.kwargs
        except JSONDecodeError as e:
            self.errors.append({"invalid_json": repr(e)})
            return None

    def _validate_fields(self, parsed_json) -> Optional[Dict]:
        validation_strategies = {
            "missing_fields": self._missing_fields,
            "invalid_fields_type": self._invalid_fields,
            "invalid_fields_constraint": self._out_of_constraint_fields
        }

        for strategy_name, strategy in validation_strategies.items():
            invalid_fields = strategy(parsed_json)
            if invalid_fields:
                self.errors.append({strategy_name: invalid_fields})

        return None if self.errors else parsed_json

    def _missing_fields(self, parsed_json):
        expected_fields = set(self.expected_fields().keys())
        actual_fields = set(parsed_json.keys())
        intersection = expected_fields.intersection(actual_fields)
        return list(expected_fields.difference(intersection))

    def _invalid_fields(self, parsed_json):
        invalid_fields = []
        for field, expected_type in self.expected_fields().items():
            value = parsed_json.get(field)
            if value is None or isinstance(value, expected_type):
                continue
            try:
                parsed_json[field] = expected_type(value)
            except Exception as e:
                invalid_fields.append({field: f"Not a valid {expected_type}. Error={repr(e)}"})
        return invalid_fields

    def _out_of_constraint_fields(self, parsed_json):
        invalid_fields = []
        for field, constraint in self.fields_constraints().items():
            value = parsed_json.get(field)
            if value is None:
                continue
            within_constraint = constraint.func(value)
            if not within_constraint:
                invalid_fields.append({field: f"Out of constraint: {constraint.message}"})
        return invalid_fields


class NotValidated(Exception):
    def __init__(self):
        super().__init__(f"Cannot access request data. Must call {Request.is_valid.__qualname__} first.")
