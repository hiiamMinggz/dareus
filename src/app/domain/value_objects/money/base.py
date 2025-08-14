from dataclasses import dataclass

from app.domain.value_objects.base import ValueObject
from decimal import Decimal
from app.domain.value_objects.money.constants import ZERO_MONEY
from app.domain.exceptions.base import DomainFieldError
from functools import total_ordering

@total_ordering
@dataclass(frozen=True, repr=False)
class Money(ValueObject):
    """raises DomainFieldError"""

    amount: Decimal
    
    def __post_init__(self) -> None:
        super().__post_init__()
        self._validate_money()

    def __eq__(self, other: object) -> bool:
        if not isinstance(other, Money):
            return NotImplemented
        return self.amount == other.amount

    def __lt__(self, other: object) -> bool:
        if not isinstance(other, Money):
            return NotImplemented
        return self.amount < other.amount

    def _validate_money(self) -> None:
        if self.amount < ZERO_MONEY:
            raise DomainFieldError("Money cannot be negative")
    
    def increase(self, value: Decimal) -> "Money":
        return type(self)(amount=self.amount + value)

    def decrease(self, value: Decimal) -> "Money":
        if self.amount < value:
            raise DomainFieldError("Insufficient funds")
        return type(self)(amount=self.amount - value)
    
    @classmethod
    def zero(cls) -> "Money":
        return cls(amount=ZERO_MONEY)
    