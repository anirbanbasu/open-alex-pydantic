import json
from pathlib import Path

import pytest
from pydantic import ValidationError

from open_alex_pydantic.entities.work import Work

# Public parser symbols are intentionally imported here to enforce the contract.
from open_alex_pydantic.entities.parser import parse_work
from open_alex_pydantic.entities.exceptions import WorkParsingError

DATA_DIR = Path(__file__).parent / "data/entities"
INVALID_DIR = DATA_DIR / "invalid"


def _load_json(path: Path) -> dict:
    return json.loads(path.read_text())


def test_strict_validation_rejects_incompatible_types() -> None:
    invalid = _load_json(INVALID_DIR / "work_invalid_types.json")

    with pytest.raises(ValidationError):
        Work.model_validate(invalid)


def test_immutable_work_model_rejects_assignment() -> None:
    raw = _load_json(DATA_DIR / "w3035608373.json")
    work = Work.model_validate(raw)

    with pytest.raises((TypeError, ValidationError)):
        work.title = "Mutated title"  # type: ignore[misc]


def test_public_parser_maps_validation_failures_to_domain_exception() -> None:
    invalid = _load_json(INVALID_DIR / "work_invalid_types.json")

    with pytest.raises(WorkParsingError) as exc_info:
        parse_work(invalid)

    assert str(exc_info.value) == "Failed to parse Work payload"
    assert isinstance(exc_info.value.cause, ValidationError)


def test_unknown_fields_do_not_fail_public_parsing() -> None:
    raw = _load_json(DATA_DIR / "w3215405033.json")
    raw["unknown_top_level"] = "extra"
    raw["primary_location"]["unknown_nested"] = "extra"

    parsed = parse_work(raw)
    assert parsed.id_ == raw["id"]


def test_alias_round_trip_serialization_uses_api_field_names() -> None:
    raw = _load_json(DATA_DIR / "w3215405033.json")
    parsed = parse_work(raw)
    dumped = parsed.model_dump(by_alias=True)

    assert "id" in dumped and "id_" not in dumped
    assert "type" in dumped and "type_" not in dumped
    if parsed.primary_location is not None:
        nested = parsed.primary_location.model_dump(by_alias=True)
        assert "license" in nested and "license_" not in nested


def test_non_conflicting_native_fields_remain_native_on_dump() -> None:
    raw = _load_json(DATA_DIR / "w3035608373.json")
    parsed = parse_work(raw)
    dumped = parsed.model_dump(by_alias=True)

    assert "has_fulltext" in dumped
    assert "cited_by_count" in dumped
