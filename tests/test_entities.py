import json
from pathlib import Path

import pytest

from open_alex_pydantic.entities.parser import parse_author, parse_work
from open_alex_pydantic.entities.work import Work

DATA_DIR = Path(__file__).parent / "data/entities"

_work_files = sorted(DATA_DIR.glob("w*.json"))
_author_files = sorted(DATA_DIR.glob("a*.json"))


def _load_json(path: Path) -> dict:
    return json.loads(path.read_text())


@pytest.mark.parametrize("json_file", _work_files, ids=[f.name for f in _work_files])
def test_parse_work(json_file: Path):
    raw = _load_json(json_file)
    parse_work(raw)


def test_parse_work_contains_expected_planned_fields() -> None:
    raw = _load_json(DATA_DIR / "w3035608373.json")
    parsed = parse_work(raw)

    assert parsed.content_urls is not None
    assert (
        parsed.content_urls.pdf == "https://content.openalex.org/works/W3035608373.pdf"
    )
    assert parsed.has_fulltext is True
    assert parsed.is_xpac is False
    assert parsed.countries_distinct_count == 3
    assert parsed.institutions_distinct_count == 7


def test_parse_work_location_ids_and_ids_mag_type() -> None:
    raw = _load_json(DATA_DIR / "w3215405033.json")
    parsed = Work.model_validate(raw)

    assert parsed.ids is not None
    assert parsed.ids.mag == "3215405033"
    assert parsed.primary_location is not None
    assert parsed.primary_location.id_ == "doi:10.1016/j.cogsys.2021.11.001"


def test_alias_round_trip_keeps_reserved_fields_with_api_names() -> None:
    raw = _load_json(DATA_DIR / "w3035608373.json")
    parsed = parse_work(raw)
    dumped = parsed.model_dump(by_alias=True)

    assert "id" in dumped and "id_" not in dumped
    assert "type" in dumped and "type_" not in dumped
    assert "primary_location" in dumped
    assert "license" in dumped["primary_location"]


def test_legacy_concepts_can_coexist_with_topics_and_keywords() -> None:
    raw = _load_json(DATA_DIR / "w3035608373.json")
    parsed = parse_work(raw)

    assert parsed.concepts is not None and len(parsed.concepts) > 0
    assert parsed.topics is not None and len(parsed.topics) > 0
    assert parsed.keywords is not None and len(parsed.keywords) > 0


@pytest.mark.parametrize(
    "json_file", _author_files, ids=[f.name for f in _author_files]
)
def test_parse_author(json_file: Path):
    raw = _load_json(json_file)
    parse_author(raw)


@pytest.mark.parametrize(
    "json_file", _author_files, ids=[f.name for f in _author_files]
)
def test_parse_author_contains_expected_fields(json_file: Path):
    raw = _load_json(json_file)
    parsed = parse_author(raw)

    assert parsed.display_name is not None
    assert parsed.id_ is not None
    assert parsed.works_count is not None
    assert parsed.cited_by_count is not None

    if parsed.summary_stats:
        assert isinstance(parsed.summary_stats.h_index, int)
        assert isinstance(parsed.summary_stats.i10_index, int)
        assert isinstance(parsed.summary_stats.two_year_mean_citedness, float)

    assert parsed.affiliations is not None
    assert len(parsed.affiliations) > 0

    assert parsed.last_known_institutions is not None
    assert len(parsed.last_known_institutions) > 0


@pytest.mark.parametrize(
    "json_file", _author_files, ids=[f.name for f in _author_files]
)
def test_parse_author_topics_structure(json_file: Path):
    raw = _load_json(json_file)
    parsed = parse_author(raw)

    if parsed.topics and len(parsed.topics) > 0:
        topic = parsed.topics[0]
        assert topic.id_ is not None
        assert topic.display_name is not None
        assert topic.count is not None
        assert isinstance(topic.count, int)


@pytest.mark.parametrize(
    "json_file", _author_files, ids=[f.name for f in _author_files]
)
def test_parse_author_x_concepts_structure(json_file: Path):
    raw = _load_json(json_file)
    parsed = parse_author(raw)

    if parsed.x_concepts and len(parsed.x_concepts) > 0:
        concept = parsed.x_concepts[0]
        assert concept.id_ is not None
        assert concept.display_name is not None
        assert hasattr(concept, "score")


@pytest.mark.parametrize(
    "json_file", _author_files, ids=[f.name for f in _author_files]
)
def test_parse_author_round_trip_by_alias(json_file: Path):
    raw = _load_json(json_file)
    parsed = parse_author(raw)
    dumped = parsed.model_dump(by_alias=True)

    assert "id" in dumped
    assert "type" not in dumped  # No direct type field at author level


@pytest.mark.parametrize(
    "json_file", _author_files, ids=[f.name for f in _author_files]
)
def test_parse_author_institution_structure(json_file: Path):
    raw = _load_json(json_file)
    parsed = parse_author(raw)

    if parsed.affiliations and len(parsed.affiliations) > 0:
        # Check the nested institution object inside first affiliation
        first_aff = parsed.affiliations[0]
        if hasattr(first_aff, "institution") and first_aff.institution:
            assert first_aff.institution.id_ is not None

            # Verify round-trip keeps API field names
            dumped = parsed.model_dump(by_alias=True)
            assert "id" in dumped["affiliations"][0]["institution"]
