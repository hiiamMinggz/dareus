from dataclasses import dataclass
import re

from app.domain.value_objects.base import ValueObject
from app.domain.value_objects.email.constants import EMAIL_PATTERN, EMAIL_MAX_LEN
from app.domain.exceptions.base import DomainFieldError

@dataclass(frozen=True, repr=False)
class Email(ValueObject):
    """raises DomainFieldError"""

    value: str

    def __post_init__(self) -> None:
        super().__post_init__()
        self._validate_email()

    def _validate_email(self) -> None:
        if not re.match(EMAIL_PATTERN, self.value):
            raise DomainFieldError(f"Invalid email: {self.value}")
        if len(self.value) > EMAIL_MAX_LEN:
            raise DomainFieldError(f"Email is too long: {self.value}")
