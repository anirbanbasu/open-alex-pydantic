import json
from pathlib import Path

import pytest

from open_alex_pydantic.entities.parser import parse_work
from open_alex_pydantic.entities.work import Work

DATA_DIR = Path(__file__).parent / "data/entities"

_work_files = sorted(DATA_DIR.glob("w*.json"))


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
