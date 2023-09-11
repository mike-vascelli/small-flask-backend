import uuid
from typing import Dict, Any

from deserializers.request import Request, Constraint


class CreationRequest(Request):
    def expected_fields(self) -> Dict[str, Any]:
        return {"pk": uuid.UUID}

    def fields_constraints(self) -> Dict[str, Constraint]:
        return {}
