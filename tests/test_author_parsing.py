"""Tests for Author model parsing functionality."""

import pytest
from pydantic import ValidationError

from open_alex_pydantic.entities.parser import parse_author
from open_alex_pydantic.entities.exceptions import AuthorParsingError

# Test fixtures directory
DATA_DIR = "tests/data/entities"


def _load_json(path: str) -> dict:
    import json

    with open(path, "r") as f:
        return json.load(f)


@pytest.fixture
def valid_author_payload():
    """Provide a valid author payload from test data."""
    return _load_json(f"{DATA_DIR}/a5029727898.json")


# =============================================================================
# User Story 1 - Tests for parsing documented Author payloads end-to-end (P1 - MVP)
# =============================================================================


@pytest.mark.parametrize("author_file", ["a5029727898.json", "a5043883509.json"])
def test_parse_author_valid_payloads(author_file: str):
    """US1. Parse Author payloads successfully."""
    payload = _load_json(f"{DATA_DIR}/{author_file}")
    parsed = parse_author(payload)

    assert parsed.id_ is not None
    assert parsed.display_name is not None


def test_parse_author_summary_stats_fields(valid_author_payload):
    """US1. Verify summary_stats fields are parsed correctly."""
    parsed = parse_author(valid_author_payload)

    assert parsed.summary_stats is not None
    assert isinstance(parsed.summary_stats.h_index, int)
    assert isinstance(parsed.summary_stats.i10_index, int)
    # Note: API uses '2yr_mean_citedness' but we alias to 'two_year_mean_citedness'
    assert hasattr(parsed.summary_stats, "two_year_mean_citedness")
    assert isinstance(parsed.summary_stats.two_year_mean_citedness, float)


def test_parse_author_nested_affiliations(valid_author_payload):
    """US1. Verify affiliations are parsed as nested Institution objects."""
    parsed = parse_author(valid_author_payload)

    assert parsed.affiliations is not None
    assert len(parsed.affiliations) > 0

    first_aff = parsed.affiliations[0]
    assert hasattr(first_aff, "institution")
    assert first_aff.institution is not None
    assert isinstance(first_aff.institution.id_, str)


def test_parse_author_topics_with_hierarchy(valid_author_payload):
    """US1. Verify topics are parsed with subfield/field/domain hierarchy."""
    parsed = parse_author(valid_author_payload)

    if parsed.topics and len(parsed.topics) > 0:
        topic = parsed.topics[0]
        assert topic.id_ is not None
        assert topic.display_name is not None

        # Check hierarchy objects exist
        if topic.subfield:
            assert isinstance(topic.subfield.id_, str)
        if topic.field:
            assert isinstance(topic.field.id_, str)
        if topic.domain:
            assert isinstance(topic.domain.id_, str)


# =============================================================================
# User Story 2 - Tests for native naming with reserved keyword aliases (P2)
# =============================================================================


def test_alias_round_trip_uses_api_field_names(valid_author_payload):
    """US2. Round-trip serialization uses API field names (id, type)."""
    parsed = parse_author(valid_author_payload)
    dumped = parsed.model_dump(by_alias=True)

    # Top level: id should appear, not id_
    assert "id" in dumped
    assert "id_" not in dumped

    # For nested institutions: type should appear, not type_
    if parsed.affiliations and len(parsed.affiliations) > 0:
        first_aff = parsed.affiliations[0]
        if hasattr(first_aff, "institution") and first_aff.institution:
            nested = first_aff.institution.model_dump(by_alias=True)
            assert "type" in nested
            assert "type_" not in nested


def test_non_conflicting_native_fields_remain_native(valid_author_payload):
    """US2. Non-conflicting fields remain as native snake_case."""
    parsed = parse_author(valid_author_payload)
    dumped = parsed.model_dump(by_alias=True)

    # These should all be native names (no aliasing needed)
    assert "display_name" in dumped
    assert "orcid" in dumped
    assert "works_count" in dumped
    assert "cited_by_count" in dumped


# =============================================================================
# User Story 3 - Tests for domain-level exception handling (P3)
# =============================================================================


def test_immutable_author_model_rejects_assignment(valid_author_payload):
    """US3. Author model is immutable - assignment fails."""
    parsed = parse_author(valid_author_payload)

    with pytest.raises(ValidationError):
        parsed.display_name = "Mutated name"


def test_strict_validation_rejects_incompatible_types():
    """US3. Strict mode rejects incompatible types without coercion."""
    valid = _load_json(f"{DATA_DIR}/a5029727898.json")

    # Make h_index a string instead of int - should fail in strict mode
    invalid = valid.copy()
    invalid["summary_stats"] = {
        "h_index": "19",  # String instead of integer
        "i10_index": 35,
        "2yr_mean_citedness": 0.0,
    }

    with pytest.raises(AuthorParsingError) as exc_info:
        parse_author(invalid)

    assert str(exc_info.value) == "Failed to parse Author payload"
    assert isinstance(exc_info.value.cause, ValidationError)


def test_unknown_fields_do_not_fail_parsing():
    """US3. Extra fields are tolerated (extra='allow')."""
    payload = _load_json(f"{DATA_DIR}/a5029727898.json")

    # Add unknown field at top level
    payload["unknown_top_level_field"] = "should_not_fail"

    # Should parse successfully despite extra field
    parsed = parse_author(payload)
    assert parsed.id_ is not None
