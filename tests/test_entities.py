import json
from pathlib import Path

import pytest

from open_alex_pydantic.entities.work import Work

DATA_DIR = Path(__file__).parent / "data/entities"

_work_files = sorted(DATA_DIR.glob("w*.json"))


@pytest.mark.parametrize("json_file", _work_files, ids=[f.name for f in _work_files])
def test_parse_work(json_file: Path):
    raw = json.loads(json_file.read_text())
    Work.model_validate(raw)
