from dataclasses import dataclass

from app.domain.value_objects.base import ValueObject
from app.domain.exceptions.base import DomainFieldError
from functools import total_ordering

from app.domain.value_objects.text.constants import MAX_TITLE_LEN, MIN_TITLE_LEN

@total_ordering
@dataclass(frozen=True, repr=False)
class Title(ValueObject):
    """raises DomainFieldError"""

    value: str

    def __post_init__(self) -> None:
        super().__post_init__()
        self._validate_title()

    def _validate_title(self) -> None:
        if len(self.value) < MIN_TITLE_LEN:
            raise DomainFieldError("Title is too short")
        if len(self.value) > MAX_TITLE_LEN:
            raise DomainFieldError("Title is too long")

        