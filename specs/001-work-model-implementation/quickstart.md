# Quickstart: Validate Work Model Alignment

## Prerequisites

- Python 3.12+
- Project dependencies installed

## Setup

From repository root:

```bash
uv sync
```

If using the existing virtual environment workflow:

```bash
source .venv/bin/activate
```

## Validation Workflow (TDD-first)

1. Add or update failing tests first for each behavior:
   - strict validation rejections
   - immutable model behavior
   - alias remap behavior (`id/type/license`)
   - unknown-field tolerance
   - domain exception mapping via public parser
2. Run tests and confirm failures before implementation changes.
3. Implement minimal model and parser changes in source.
4. Re-run tests until all pass.
5. Confirm changed-scope coverage is 100%.

## Run Commands

Run targeted entity tests:

```bash
uv run pytest tests/test_entities.py -q
uv run pytest tests/test_work_parsing.py -q
```

Run all tests:

```bash
uv run pytest -q
```

Coverage check (changed scope must remain 100%):

```bash
uv run coverage run -m pytest -q
uv run coverage report -m
```

## Expected Outcomes

- Existing sample fixtures parse successfully after alignment.
- New tests prove strictness, immutability, alias policy, and unknown-field behavior.
- Invalid payload tests prove public parser raises domain exceptions.
- Coverage report confirms full coverage for modified/new parsing code.

## Artifact References

- Data model: `specs/001-work-model-implementation/data-model.md`
- Parsing contract: `specs/001-work-model-implementation/contracts/work-parsing-contract.md`
- Plan: `specs/001-work-model-implementation/plan.md`
