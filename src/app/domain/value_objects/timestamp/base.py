from dataclasses import dataclass

from app.domain.value_objects.base import ValueObject
from app.domain.exceptions.base import DomainFieldError
from functools import total_ordering
from datetime import datetime

@total_ordering
@dataclass(frozen=True, repr=False)
class Timestamp(ValueObject):
    """raises DomainFieldError"""

    value: datetime

    def __eq__(self, other: object) -> bool:
        if not isinstance(other, Timestamp):
            return NotImplemented
        return self.value == other.value

    def __lt__(self, other: object) -> bool:
        if not isinstance(other, Timestamp):
            return NotImplemented
        return self.value < other.value
    
    def increase(self, value: datetime) -> "Timestamp":
        return type(self)(amount=self.value + value)
    