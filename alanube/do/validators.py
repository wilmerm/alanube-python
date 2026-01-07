"""Minimal pre-request validations for Alanube API calls.

These checks only cover cases the API will certainly reject, so we fail
early instead of issuing requests that would error out anyway.
"""

from __future__ import annotations

import re
from typing import Iterable, List, Literal, Optional, overload

from .exceptions import ValidationError
from .config import (
    ALANUBE_RESPONSE_STATUS_CHOICES,
    LEGAL_STATUS_CHOICES,
)


ALLOWED_DOCUMENT_STATUSES = set(status for status, _ in ALANUBE_RESPONSE_STATUS_CHOICES)

ALLOWED_LEGAL_STATUSES = set(status for status, _ in LEGAL_STATUS_CHOICES)

ALLOWED_ENVIRONMENTS = {1, 2, 3}

IDENTIFICATION_PATTERN = re.compile(r"^(\d{9}|\d{11})$")


def _split_values(value: Optional[str | Iterable[str]], field_name: str, *, required: bool = False) -> List[str]:
    if value is None:
        if required:
            raise ValidationError(message=f"{field_name} is required.")
        return []

    if isinstance(value, str):
        values = [v.strip() for v in value.split(",") if v.strip()]
    elif isinstance(value, Iterable):
        values = []
        for item in value:
            if item is None:
                continue
            if not isinstance(item, str):
                raise ValidationError(message=f"Each {field_name} entry must be a string.")
            cleaned = item.strip()
            if cleaned:
                values.append(cleaned)
    else:
        raise ValidationError(message=f"{field_name} must be a string or iterable of strings.")

    if required and not values:
        raise ValidationError(message=f"{field_name} cannot be empty.")
    return values


def validate_document_status(status: Optional[str | Iterable[str]]) -> Optional[str]:
    statuses = _split_values(status, "status")
    for status_value in statuses:
        if status_value not in ALLOWED_DOCUMENT_STATUSES:
            raise ValidationError(message=f"Invalid status '{status_value}'. Allowed: {sorted(ALLOWED_DOCUMENT_STATUSES)}")
    return ",".join(statuses) if statuses else None


@overload
def validate_legal_status(
    legal_status: Optional[str | Iterable[str]],
    *,
    required: Literal[True],
) -> str:
    ...


@overload
def validate_legal_status(
    legal_status: Optional[str | Iterable[str]],
    *,
    required: Literal[False] = False,
) -> Optional[str]:
    ...


def validate_legal_status(
    legal_status: Optional[str | Iterable[str]],
    *,
    required: bool = False,
) -> Optional[str]:
    statuses = _split_values(legal_status, "legal_status", required=required)
    for status_value in statuses:
        if status_value not in ALLOWED_LEGAL_STATUSES:
            raise ValidationError(
                message=f"Invalid legal_status '{status_value}'. Allowed: {sorted(ALLOWED_LEGAL_STATUSES)}"
            )
    return ",".join(statuses) if statuses else None


def validate_pagination(limit: Optional[int], page: Optional[int]):
    for name, value in (("limit", limit), ("page", page)):
        if value is None:
            continue
        if not isinstance(value, int):
            raise ValidationError(message=f"{name} must be an integer.")
        if value <= 0:
            raise ValidationError(message=f"{name} must be greater than zero.")


def validate_identification_number(identification: Optional[str], field_name: str = "identification"):
    if identification is None:
        return
    if not isinstance(identification, str):
        raise ValidationError(message=f"{field_name} must be a string.")
    if not IDENTIFICATION_PATTERN.match(identification):
        raise ValidationError(message=f"{field_name} must contain 9 or 11 digits with no separators.")


def validate_environment(environment: Optional[int]):
    if environment is None:
        return
    if not isinstance(environment, int):
        raise ValidationError(message="environment must be an integer (1, 2, or 3).")
    if environment not in ALLOWED_ENVIRONMENTS:
        raise ValidationError(message="environment must be one of 1 (PreCertificacion), 2 (Produccion), or 3 (Certificacion).")
