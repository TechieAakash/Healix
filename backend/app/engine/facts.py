from __future__ import annotations
from enum import Enum
from typing import Any, Optional, Dict
from pydantic import BaseModel, Field
import uuid
import datetime

class FactValue(str, Enum):
    TRUE = "TRUE"
    FALSE = "FALSE"
    UNKNOWN = "UNKNOWN"
    NOT_ASKED = "NOT_ASKED"
    NOT_APPLICABLE = "NOT_APPLICABLE"

    @classmethod
    def from_bool(cls, b: Optional[bool]) -> FactValue:
        if b is True:
            return cls.TRUE
        elif b is False:
            return cls.FALSE
        return cls.UNKNOWN

    def to_bool(self) -> Optional[bool]:
        if self == FactValue.TRUE:
            return True
        elif self == FactValue.FALSE:
            return False
        return None

class Fact(BaseModel):
    id: str = Field(default_factory=lambda: str(uuid.uuid4()))
    name: str                        # e.g., "symptom.headache.throbbing"
    value: FactValue
    certainty: float = 1.0           # 0.0 to 1.0
    data_type: str = "boolean"       # boolean, numeric, categorical, text
    raw_value: Optional[Any] = None  # e.g., 38.5, "unilateral"
    source: str = "USER_REPORTED"    # USER_REPORTED | DERIVED | INFERRED | SYSTEM
    timestamp: datetime.datetime = Field(default_factory=lambda: datetime.datetime.now(datetime.timezone.utc))
    metadata: Dict[str, Any] = Field(default_factory=dict)

    def is_definitely_true(self) -> bool:
        return self.value == FactValue.TRUE

    def is_definitely_false(self) -> bool:
        return self.value == FactValue.FALSE

    def is_known(self) -> bool:
        return self.value in (FactValue.TRUE, FactValue.FALSE)

    def is_missing(self) -> bool:
        return self.value in (FactValue.UNKNOWN, FactValue.NOT_ASKED)

