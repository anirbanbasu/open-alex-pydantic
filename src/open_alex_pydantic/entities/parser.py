from __future__ import annotations

from collections.abc import Mapping
from typing import Any

from pydantic import ValidationError

from open_alex_pydantic.entities.exceptions import AuthorParsingError, WorkParsingError
from open_alex_pydantic.entities.author import Author
from open_alex_pydantic.entities.work import Work


def parse_work(payload: Mapping[str, Any]) -> Work:
    """Parse a raw OpenAlex Work payload into a validated Work model."""

    try:
        return Work.model_validate(payload)
    except ValidationError as exc:
        raise WorkParsingError("Failed to parse Work payload", cause=exc) from exc


def parse_author(payload: Mapping[str, Any]) -> Author:
    """Parse a raw OpenAlex Author payload into a validated Author model."""

    try:
        return Author.model_validate(payload)
    except ValidationError as exc:
        raise AuthorParsingError("Failed to parse Author payload", cause=exc) from exc
