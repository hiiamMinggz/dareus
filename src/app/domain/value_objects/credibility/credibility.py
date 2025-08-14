from dataclasses import dataclass
import re

from app.domain.value_objects.base import ValueObject
from app.domain.value_objects.credibility.constants import MAX_CREDIT, ZERO_CREDIT
from app.domain.exceptions.base import DomainFieldError

@dataclass(frozen=True, repr=False)
class Credibility(ValueObject):
    """raises DomainFieldError"""

    value: float

    def __post_init__(self) -> None:
        super().__post_init__()
        self._validate_credibility()

    def _validate_credibility(self) -> None:
        if self.value > MAX_CREDIT:
            raise DomainFieldError(f"Credibility cannot be greater than {MAX_CREDIT}")
        if self.value < ZERO_CREDIT:
            raise DomainFieldError(f"Credibility cannot be less than {ZERO_CREDIT}")
    
    def increase(self, value: float) -> "Credibility":
        return type(self)(amount=self.amount + value)

    def decrease(self, value: float) -> "Credibility":
        if self.amount < value:
            raise DomainFieldError("Insufficient funds")
        return type(self)(amount=self.amount - value)

    @classmethod
    def zero(cls) -> "Credibility":
        return cls(value=ZERO_CREDIT)
    def max(cls) -> "Credibility":
        return cls(value=MAX_CREDIT)
    
    
        



