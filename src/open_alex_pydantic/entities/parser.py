from collections.abc import Mapping
from typing import Any

from pydantic import ValidationError

from open_alex_pydantic.entities.exceptions import WorkParsingError
from open_alex_pydantic.entities.work import Work


def parse_work(payload: Mapping[str, Any]) -> Work:
    """Parse a raw OpenAlex Work payload into a validated Work model."""

    try:
        return Work.model_validate(payload)
    except ValidationError as exc:
        raise WorkParsingError("Failed to parse Work payload", cause=exc) from exc
