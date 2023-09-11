import uuid
from typing import Dict, Any

from deserializers.request import Request, Constraint

progress_constraint = Constraint(func=lambda p: 0 <= p <= 1.0, message="0 <= progress <= 1.0")


class UpdateRequest(Request):
    def expected_fields(self) -> Dict[str, Any]:
        return {"pk": uuid.UUID, "progress": float}

    def fields_constraints(self) -> Dict[str, Constraint]:
        return {"progress": progress_constraint}
