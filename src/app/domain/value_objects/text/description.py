from dataclasses import dataclass

from app.domain.value_objects.base import ValueObject
from app.domain.exceptions.base import DomainFieldError
from functools import total_ordering

from app.domain.value_objects.text.constants import MAX_DESCRIPTION_LEN

@total_ordering
@dataclass(frozen=True, repr=False)
class Description(ValueObject):
    """raises DomainFieldError"""

    value: str

    def __post_init__(self) -> None:
        super().__post_init__()
        self._validate_description()

    def _validate_description(self) -> None:
        if isinstance(self.value, None):
            self.value = ""
        if len(self.value) > MAX_DESCRIPTION_LEN:
            raise DomainFieldError("Description is too long")

        