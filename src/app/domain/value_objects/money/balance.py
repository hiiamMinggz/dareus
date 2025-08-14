from dataclasses import dataclass
from functools import total_ordering

from app.domain.value_objects.money.base import Money

@total_ordering
@dataclass(frozen=True, repr=False)
class Balance(Money):
    """raises DomainFieldError"""

