# Tasks: Work Model Implementation Alignment

**Input**: Design documents from `/specs/001-work-model-implementation/`

**Prerequisites**: plan.md (required), spec.md (required for user stories), research.md, data-model.md, contracts/

**Tests**: Test tasks are REQUIRED. Follow strict TDD and maintain 100% coverage for all new and modified code.

**Organization**: Tasks are grouped by user story to enable independent implementation and testing of each story.

## Format: `[ID] [P?] [Story] Description`

- **[P]**: Can run in parallel (different files, no dependencies)
- **[Story]**: Which user story this task belongs to (e.g., US1, US2, US3)
- Include exact file paths in descriptions

## Path Conventions

- Single project paths are used: `src/` and `tests/` at repository root.

## Phase 1: Setup (Shared Infrastructure)

**Purpose**: Prepare fixture and test scaffolding for strict TDD execution.

- [x] T001 Create invalid Work payload fixture directory and baseline invalid fixture in tests/data/entities/invalid/work_invalid_types.json [Trace: FR-010, SC-002, FR-011]
- [x] T002 [P] Add parsing-boundary test module scaffold in tests/test_work_parsing.py [Trace: FR-010, SC-002, FR-011]
- [x] T003 [P] Add fixture loader helper for valid and invalid Work payloads in tests/test_entities.py [Trace: FR-011]

---

## Phase 2: Foundational (Blocking Prerequisites)

**Purpose**: Core parsing and model infrastructure that must be complete before story implementation.

**⚠️ CRITICAL**: No user story work can begin until this phase is complete.

- [x] T004 [P] Add foundational failing tests for immutability and strict validation behavior in tests/test_work_parsing.py
- [x] T005 [P] Add foundational failing test for domain exception mapping contract in tests/test_work_parsing.py
- [x] T006 Implement strict/frozen/extra-allow shared model configuration in src/open_alex_pydantic/entities/base.py
- [x] T007 [P] Add domain parsing exception class for Work parsing failures in src/open_alex_pydantic/entities/exceptions.py
- [x] T008 Implement public parse boundary that maps validation errors to domain exceptions in src/open_alex_pydantic/entities/parser.py
- [x] T009 Export foundational parsing and exception symbols in src/open_alex_pydantic/entities/__init__.py

**Checkpoint**: Foundation ready - user story implementation can now begin.

---

## Phase 3: User Story 1 - Parse documented Work payloads end-to-end (Priority: P1) 🎯 MVP

**Goal**: Ensure documented Work payloads parse successfully with complete nested model coverage.

**Independent Test**: Parse `tests/data/entities/w3035608373.json` and `tests/data/entities/w3215405033.json` via public parser and assert expected typed fields across top-level and nested structures.

### Tests for User Story 1 (REQUIRED) ⚠️

- [x] T010 [P] [US1] Add failing end-to-end parse assertions for both sample payloads in tests/test_entities.py
- [x] T011 [P] [US1] Add failing tests for planned schema fields (`content_urls`, `has_fulltext`, `is_xpac`, distinct counts) in tests/test_entities.py
- [x] T012 [P] [US1] Add failing tests for nested location/source/ids shape alignment and `ids.mag` type expectations in tests/test_entities.py

### Implementation for User Story 1

- [x] T013 [US1] Add/adjust Work nested entity fields for documented fixture compatibility in src/open_alex_pydantic/entities/work.py
- [x] T014 [US1] Add top-level Work fields for documented counters and content URL object in src/open_alex_pydantic/entities/work.py
- [x] T015 [US1] Update WorkIds and Location schemas for strict-compatible payload typing in src/open_alex_pydantic/entities/work.py
- [x] T016 [US1] Update parse tests to call public parse boundary for end-to-end validation in tests/test_entities.py

**Checkpoint**: User Story 1 should be fully functional and independently testable.

---

## Phase 4: User Story 2 - Preserve native schema naming with safe Python access (Priority: P2)

**Goal**: Enforce native snake_case mapping with explicit conflict-only alias remaps and stable round-trip serialization.

**Independent Test**: Parse payloads with reserved-name fields and assert access via trailing-underscore fields while serialized output uses native API names.

### Tests for User Story 2 (REQUIRED) ⚠️

- [x] T017 [P] [US2] Add failing alias parse/dump round-trip tests for `id`, `type`, and `license` mappings in tests/test_entities.py
- [x] T018 [P] [US2] Add failing tests ensuring non-conflicting native snake_case fields remain unchanged in tests/test_entities.py

### Implementation for User Story 2

- [x] T019 [US2] Normalize explicit alias declarations for reserved/built-in conflict fields in src/open_alex_pydantic/entities/work.py
- [x] T020 [US2] Configure shared model alias behavior for stable parse and by-alias serialization in src/open_alex_pydantic/entities/base.py
- [x] T021 [US2] Add focused serialization assertions tied to public parser outputs in tests/test_work_parsing.py

**Checkpoint**: User Story 2 should be independently testable and preserve naming policy guarantees.

---

## Phase 5: User Story 3 - Return stable domain-level failures on invalid payloads (Priority: P3)

**Goal**: Ensure invalid payloads raise domain exceptions and unknown additive fields do not fail parsing.

**Independent Test**: Parse invalid fixtures through public parser and assert domain exceptions; parse payloads with unknown fields and assert successful parsing.

### Tests for User Story 3 (REQUIRED) ⚠️

- [x] T022 [P] [US3] Add failing invalid-payload tests for domain exception behavior in tests/test_work_parsing.py
- [x] T023 [P] [US3] Add failing unknown-field tolerance tests for additive payload properties in tests/test_work_parsing.py
- [x] T024 [P] [US3] Add failing tests for exception message/cause contract stability in tests/test_work_parsing.py

### Implementation for User Story 3

- [x] T025 [US3] Finalize parse exception wrapping semantics and cause retention in src/open_alex_pydantic/entities/parser.py
- [x] T026 [US3] Finalize unknown-field behavior and strictness interplay in src/open_alex_pydantic/entities/base.py
- [x] T027 [US3] Add or refine invalid fixture payloads used by exception tests in tests/data/entities/invalid/work_invalid_types.json

**Checkpoint**: User Story 3 should be independently testable with stable domain exception behavior.

---

## Phase 6: Polish & Cross-Cutting Concerns

**Purpose**: Cross-story hardening, docs alignment, and coverage closure.

- [x] T028 [P] Add regression assertions for legacy/deprecated compatibility (`concepts` with topics/keywords) in tests/test_entities.py
- [x] T029 [P] Update quickstart validation steps with final test and coverage commands in specs/001-work-model-implementation/quickstart.md
- [x] T030 Update package usage docs for public parser and domain exception handling in README.md [Trace: FR-010, QV-006, Constitution IV/V]
- [x] T031 Run full suite and enforce 100% coverage for changed scope, documenting final checks in tests/test_work_parsing.py

---

## Dependencies & Execution Order

### Phase Dependencies

- **Setup (Phase 1)**: No dependencies - can start immediately.
- **Foundational (Phase 2)**: Depends on Setup completion - blocks all user stories.
- **User Stories (Phase 3+)**: Depend on Foundational completion.
- **Polish (Phase 6)**: Depends on all user stories being complete.

### User Story Dependencies

- **User Story 1 (P1)**: Starts after Foundational completion.
- **User Story 2 (P2)**: Starts after Foundational completion; can run independently but may reuse US1 model updates.
- **User Story 3 (P3)**: Starts after Foundational completion; depends on public parser availability from Foundational tasks.

### Within Each User Story

- Tests MUST be written and fail first.
- Model/config implementation follows failing tests.
- Public parser and serialization behavior are verified before story completion.

### Parallel Opportunities

- Setup tasks marked `[P]` can run concurrently.
- Foundational tasks `T004` and `T005` can run in parallel first; `T007` can run in parallel with `T006`; `T008` depends on `T006` and `T007`.
- In US1, `T010` to `T012` can be authored in parallel.
- In US2, `T017` and `T018` can be authored in parallel.
- In US3, `T022` to `T024` can be authored in parallel.
- Polish tasks `T028` and `T029` can run in parallel.

---

## Parallel Example: User Story 1

```bash
# Author failing US1 tests in parallel:
Task: "T010 [US1] Add failing end-to-end parse assertions in tests/test_entities.py"
Task: "T011 [US1] Add failing schema field tests in tests/test_entities.py"
Task: "T012 [US1] Add failing nested shape tests in tests/test_entities.py"

# Then implement model updates sequentially:
Task: "T013 [US1] Adjust nested entities in src/open_alex_pydantic/entities/work.py"
Task: "T014 [US1] Add top-level Work fields in src/open_alex_pydantic/entities/work.py"
Task: "T015 [US1] Update WorkIds/Location typing in src/open_alex_pydantic/entities/work.py"
```

---

## Parallel Example: User Story 2

```bash
# Author failing alias-policy tests in parallel:
Task: "T017 [US2] Add alias round-trip tests in tests/test_entities.py"
Task: "T018 [US2] Add native snake_case preservation tests in tests/test_entities.py"

# Implement alias behavior updates:
Task: "T019 [US2] Normalize alias declarations in src/open_alex_pydantic/entities/work.py"
Task: "T020 [US2] Configure alias behavior in src/open_alex_pydantic/entities/base.py"
```

---

## Parallel Example: User Story 3

```bash
# Author failing exception-boundary tests in parallel:
Task: "T022 [US3] Add invalid payload domain-exception tests in tests/test_work_parsing.py"
Task: "T023 [US3] Add unknown-field tolerance tests in tests/test_work_parsing.py"
Task: "T024 [US3] Add exception contract tests in tests/test_work_parsing.py"

# Implement parser and config refinements:
Task: "T025 [US3] Finalize parser exception wrapping in src/open_alex_pydantic/entities/parser.py"
Task: "T026 [US3] Finalize unknown-field/strictness interplay in src/open_alex_pydantic/entities/base.py"
```

---

## Implementation Strategy

### MVP First (User Story 1 Only)

1. Complete Setup and Foundational phases.
2. Complete User Story 1.
3. Validate with sample payload parsing and field assertions.
4. Stop and confirm MVP before continuing.

### Incremental Delivery

1. Deliver US1 (schema-aligned parsing).
2. Deliver US2 (alias and naming policy guarantees).
3. Deliver US3 (stable domain exception boundary).
4. Finish cross-cutting polish and coverage closure.

### Parallel Team Strategy

1. One engineer completes Foundational parser/base setup.
2. After Foundational completion:
   - Engineer A drives US1 model alignment.
   - Engineer B drives US2 alias-policy tests and updates.
   - Engineer C drives US3 exception-boundary tests and parser behavior.
3. Merge into Polish for final coverage and documentation.

---

## Notes

- All tasks use strict checklist format with IDs, optional `[P]`, and `[USx]` story labels where required.
- Tasks are specific enough for direct execution by an implementation agent.
- TDD order is enforced by placing failing-test tasks before implementation tasks in each story phase.
