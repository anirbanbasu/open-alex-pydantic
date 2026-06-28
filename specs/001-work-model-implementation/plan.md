# Implementation Plan: Work Model Implementation Alignment

**Branch**: `master` | **Date**: 2026-06-28 | **Spec**: `specs/001-work-model-implementation/spec.md`

**Input**: Feature specification from `specs/001-work-model-implementation/spec.md`

## Summary

Align the existing Work entity implementation with the OpenAlex Works schema
and the repository constitution by enforcing strict and immutable Pydantic v2
model behavior, preserving native snake_case field mappings with manual
reserved-name aliases only, tolerating additive unknown fields, and introducing
public parsing boundaries that normalize validation failures into domain
exceptions. Expand tests to follow strict TDD sequencing and enforce 100%
coverage for all touched Work parsing code paths.

## Technical Context

**Language/Version**: Python 3.12+

**Primary Dependencies**: pydantic>=2.13.4, pytest>=9.1.1, coverage>=7.14.3

**Storage**: N/A (in-memory model validation library)

**Testing**: pytest with fixture-driven JSON payload validation

**Target Platform**: Cross-platform Python package (local dev + CI)

**Project Type**: Python library

**Performance Goals**: Parse representative Work fixtures deterministically with
no meaningful regression versus current baseline and without quadratic behavior
on nested arrays.

**Constraints**:
- Strict validation must reject wrong input types (no silent coercion).
- Models must be immutable (frozen configuration).
- No global alias generator; only explicit alias remaps for reserved/built-in
  conflicts (id/type/license -> id_/type_/license_).
- Unexpected additive fields must not fail parsing by default.
- Public parsing interfaces must raise project-defined domain exceptions.

**Scale/Scope**: One primary Work aggregate with nested submodels, two existing
large sample fixtures, and focused test enhancements in `tests/test_entities.py`
plus new targeted tests.

## Constitution Check

*GATE: Must pass before Phase 0 research. Re-check after Phase 1 design.*

Pre-Design Gate Status: PASS
- TDD sequencing is explicit: failing tests for schema mismatches, strictness,
  immutability, alias behavior, and exception mapping will be added first.
- Coverage strategy is explicit: all modified/new parsing paths must stay at
  100% coverage for touched files.
- Python 3.12+, strict typing, and Pydantic v2 strict behavior are explicit in
  planned model/config updates.
- Native snake_case field mapping and manual reserved-name aliases only are
  explicit and constrained.
- Domain exception mapping at public parsing boundaries is explicit.

## Project Structure

### Documentation (this feature)

```text
specs/001-work-model-implementation/
├── plan.md
├── research.md
├── data-model.md
├── quickstart.md
├── contracts/
│   └── work-parsing-contract.md
└── tasks.md
```

### Source Code (repository root)

```text
src/
└── open_alex_pydantic/
    ├── __init__.py
    └── entities/
        ├── __init__.py
        ├── base.py
        └── work.py

tests/
├── test_entities.py
└── data/
    └── entities/
        ├── w3035608373.json
        └── w3215405033.json
```

**Structure Decision**: Keep the existing single-library structure. Implement
all Work schema and parsing-boundary changes in `src/open_alex_pydantic/entities/`
and add/extend tests under `tests/`.

## Phase 0: Research Plan

- Validate strict Pydantic v2 configuration patterns that satisfy both strict
  type enforcement and tolerant unknown-field handling.
- Reconcile observed sample payload deltas against current model fields
  (including `content_urls`, location-level `id`, and `ids.mag` typing).
- Define domain exception boundary strategy for public parsing APIs.

Output artifact: `specs/001-work-model-implementation/research.md`

## Phase 1: Design and Contracts

- Produce `data-model.md` documenting Work aggregate, nested entities, aliases,
  validation rules, and state/compatibility semantics.
- Define parsing/interface contract in `contracts/work-parsing-contract.md`.
- Produce runnable validation guide in `quickstart.md` with TDD-first flow.
- Update coding agent context marker content to reference this plan file.
- Re-run constitution gate after design artifacts are complete.

Output artifacts:
- `specs/001-work-model-implementation/data-model.md`
- `specs/001-work-model-implementation/contracts/work-parsing-contract.md`
- `specs/001-work-model-implementation/quickstart.md`

## Post-Design Constitution Check

Post-Design Gate Status: PASS
- Design artifacts require failing tests before implementation tasks.
- Coverage, strict typing, strict validation, immutability, and alias policy
  are codified in model and contract design.
- Unknown-field tolerance is explicitly handled via model extra-field policy.
- Domain exceptions are defined as a required public parsing contract.

## Complexity Tracking

No constitution violations or complexity exemptions are required.
