"""
- Flat (non-nested) models are best kept anemic (without methods).
  The behavior of such models is described in the domain service.

- When working with non-flat models, such as aggregates, it makes sense
  to have rich models (with methods). The behavior of these models is
  described within the models themselves.
"""

from dataclasses import dataclass
from typing import Optional
from app.domain.entities.base import Entity
from app.domain.enums.challenge_status import ChallengeStatus
from app.domain.enums.fee import Fee
from app.domain.exceptions.base import DomainError
from app.domain.value_objects.challenge_id import ChallengeId
from app.domain.value_objects.money.challenge_amount import ChallengeAmount
from app.domain.value_objects.money.streamer_fixed_amount import StreamerFixedAmount
from app.domain.value_objects.text.description import Description
from app.domain.value_objects.text.title import Title
from app.domain.value_objects.user_id import UserId
from app.domain.value_objects.timestamp.base import Timestamp


@dataclass(eq=False, kw_only=True)
class Challenge(Entity[ChallengeId]):
    title: Title
    description: Optional[Description]
    created_by: UserId
    assigned_to: UserId
    amount: ChallengeAmount
    fee: Fee.DEFAULT_CHALLENGE_FEE
    streamer_fixed_amount: StreamerFixedAmount
    status: ChallengeStatus
    created_at: Timestamp
    expires_at: Timestamp
    accepted_at: Timestamp

    def __post_init__(self) -> None:
        super().__post_init__()
        self._validate_challenge()

    def _validate_challenge(self) -> None:
        if self.amount < self.streamer_fixed_amount:
            raise DomainError("Challenge amount cannot be less than streamer fixed amount")
        if self.created_at > self.expires_at:
            raise DomainError("Created at cannot be greater than expires at")
        if self.accepted_at > self.expires_at:
            raise DomainError("Accepted at cannot be greater than expires at")
