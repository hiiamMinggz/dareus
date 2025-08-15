from decimal import Decimal
from unittest.mock import MagicMock

import pytest

from app.domain.entities.user import User
from app.domain.enums.user_type import UserRole, UserType
from app.domain.exceptions.base import DomainFieldError
from app.domain.exceptions.user import (
    ActivationChangeNotPermittedError,
    RoleAssignmentNotPermittedError,
    RoleChangeNotPermittedError,
)
from app.domain.services.user import UserService
from app.domain.value_objects.money.user_balance import UserBalance
from tests.app.unit.factories.value_objects import (
    create_balance,
    create_credibility,
    create_email,
    create_password_hash,
    create_raw_password,
    create_user_id,
    create_username,
)


@pytest.mark.parametrize(
    "role",
    [UserRole.USER, UserRole.ADMIN],
)

@pytest.mark.parametrize(
    "user_type",
    [UserType.VIEWER, UserType.STREAMER],
)
def test_creates_active_user_with_hashed_password(
    role: UserRole,
    user_type: UserType,
    user_id_generator: MagicMock,
    password_hasher: MagicMock,
) -> None:
    # Arrange
    username = create_username()
    raw_password = create_raw_password()

    expected_id = create_user_id()
    expected_hash = create_password_hash()
    expected_email = create_email()
    expected_credibility = create_credibility()
    expected_balance = create_balance()

    user_id_generator.return_value = expected_id.value
    password_hasher.hash.return_value = expected_hash.value
    sut = UserService(user_id_generator, password_hasher)

    # Act
    result = sut.create_user(
        username=username,
        raw_password=raw_password,
        email=expected_email,
        role=role,
        user_type=user_type,
        credibility=expected_credibility,
        balance=expected_balance,
        locked=False,
    )

    # Assert
    assert isinstance(result, User)
    assert result.id_ == expected_id
    assert result.username == username
    assert result.password_hash == expected_hash
    assert result.role == role
    assert result.locked is False
    assert result.email == expected_email
    assert result.credibility == expected_credibility
    assert result.balance == expected_balance
    assert result.user_type == user_type

@pytest.mark.parametrize(
    "role",
    [UserRole.USER, UserRole.ADMIN],
)

@pytest.mark.parametrize(
    "user_type",
    [UserType.VIEWER, UserType.STREAMER],
)
def test_creates_locked_user_if_specified(
    role: UserRole,
    user_type: UserType,
    user_id_generator: MagicMock,
    password_hasher: MagicMock,
) -> None:
    # Arrange
    username = create_username()
    raw_password = create_raw_password()

    expected_id = create_user_id()
    expected_hash = create_password_hash()
    expected_email = create_email()
    expected_credibility = create_credibility()
    expected_balance = create_balance()

    user_id_generator.return_value = expected_id.value
    password_hasher.hash.return_value = expected_hash.value
    sut = UserService(user_id_generator, password_hasher)

    # Act
    result = sut.create_user(
        username=username,
        raw_password=raw_password,
        email=expected_email,
        role=role,
        user_type=user_type,
        credibility=expected_credibility,
        balance=expected_balance,
        locked=True,
    )

    # Assert
    assert result.locked is True

@pytest.mark.parametrize(
    "role",
    [UserRole.USER, UserRole.ADMIN],
)

@pytest.mark.parametrize(
    "user_type",
    [UserType.VIEWER, UserType.STREAMER],
)
def test_creates_active_user_with_invalid_balance(
    role: UserRole,
    user_type: UserType,
    user_id_generator: MagicMock,
    password_hasher: MagicMock,
) -> None:
    # Arrange
    username = create_username()
    raw_password = create_raw_password()

    expected_id = create_user_id()
    expected_hash = create_password_hash()
    valid_email = create_email()
    valid_credibility = create_credibility()

    user_id_generator.return_value = expected_id.value
    password_hasher.hash.return_value = expected_hash.value
    sut = UserService(user_id_generator, password_hasher)

    # Act
    with pytest.raises(DomainFieldError, match="Money cannot be negative"):
        sut.create_user(
            username=username,
            raw_password=raw_password,
            email=valid_email,
            role=role,
            user_type=user_type,
            credibility=valid_credibility,
            balance=create_balance(value=Decimal("-10.000")),
            locked=False
        )

@pytest.mark.parametrize(
    "role",
    [UserRole.USER, UserRole.ADMIN],
)

@pytest.mark.parametrize(
    "user_type",
    [UserType.VIEWER, UserType.STREAMER],
)
def test_increases_balance(
    role: UserRole,
    user_type: UserType,
    user_id_generator: MagicMock,
    password_hasher: MagicMock,
) -> None:
    # Arrange
    username = create_username()
    raw_password = create_raw_password()

    expected_id = create_user_id()
    expected_hash = create_password_hash()
    valid_email = create_email()
    valid_credibility = create_credibility()
    valid_balance = create_balance(value=Decimal("10.000"))

    user_id_generator.return_value = expected_id.value
    password_hasher.hash.return_value = expected_hash.value
    sut = UserService(user_id_generator, password_hasher)

    # Act
    user = sut.create_user(
        username=username,
        raw_password=raw_password,
        email=valid_email,
        role=role,
        user_type=user_type,
        credibility=valid_credibility,
        balance=valid_balance,
        locked=False,
    )

    sut.increase_balance(user=user, amount=Decimal("10.000"))

    # Assert
    assert user.balance == UserBalance(amount=Decimal("20.000"))


@pytest.mark.parametrize(
    "role",
    [UserRole.USER, UserRole.ADMIN],
)

@pytest.mark.parametrize(
    "user_type",
    [UserType.VIEWER, UserType.STREAMER],
)
def test_decrease_insufficient_funds(
    role: UserRole,
    user_type: UserType,
    user_id_generator: MagicMock,
    password_hasher: MagicMock,
) -> None:
    # Arrange
    username = create_username()
    raw_password = create_raw_password()

    expected_id = create_user_id()
    expected_hash = create_password_hash()
    valid_email = create_email()
    valid_credibility = create_credibility()
    valid_balance = create_balance(value=Decimal("10.000"))

    user_id_generator.return_value = expected_id.value
    password_hasher.hash.return_value = expected_hash.value
    sut = UserService(user_id_generator, password_hasher)

    # Act
    user = sut.create_user(
        username=username,
        raw_password=raw_password,
        email=valid_email,
        role=role,
        user_type=user_type,
        credibility=valid_credibility,
        balance=valid_balance,
        locked=False,
    )
    # Assert
    with pytest.raises(DomainFieldError, match="Insufficient funds"):
        sut.decrease_balance(user=user, amount=Decimal("20.000"))
