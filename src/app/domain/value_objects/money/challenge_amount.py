from dataclasses import dataclass
from functools import total_ordering

from app.domain.exceptions.base import DomainFieldError
from app.domain.value_objects.money.base import Money
from app.domain.value_objects.money.constants import MIN_CHALLENGE_AMOUNT

@total_ordering
@dataclass(frozen=True, repr=False)
class ChallengeAmount(Money):
    """raises DomainFieldError"""
    def __post_init__(self) -> None:
        super().__post_init__()
        self._validate_challenge_amount()

    def _validate_challenge_amount(self) -> None:
        if self.amount < MIN_CHALLENGE_AMOUNT:
            raise DomainFieldError("Challenge amount cannot be less than 10.000")

