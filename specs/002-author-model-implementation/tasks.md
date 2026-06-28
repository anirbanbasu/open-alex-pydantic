# Tasks: Author Model Implementation

**Input**: Design documents from `/specs/002-author-model-implementation/`

**Prerequisites**: plan.md (required), spec.md (required for user stories)

**Tests**: Test tasks are REQUIRED. Follow strict TDD and maintain 100% coverage for all new and modified code.

**Organization**: Tasks are grouped by user story to enable independent implementation and testing of each story.

## Format: `[ID] [P?] [Story] Description`

- **Checkbox**: `- [ ]` (markdown checkbox that starts incomplete)
- **ID**: Sequential number (T001, T002, etc.)
- **[P]**: Parallelizable marker - only if task can run concurrently with others
- **[Story]**: Which user story this task belongs to (e.g., [US1], [US2], [US3])
- Include exact file paths in descriptions

## Path Conventions

- Single project paths are used: `src/` and `tests/` at repository root.

---

## Phase 1: Setup (Shared Infrastructure)

**Purpose**: Prepare fixture and test scaffolding for strict TDD execution.

- [X] T001 Create Author model source file at `src/open_alex_pydantic/entities/author.py` with all nested entity classes (AuthorIds, Institution, Affiliation, LastKnownInstitution, SummaryStats, TopicHierarchyEntry, Topic, XConceptsEntry, CountsByYearEntry)
- [ ] T002 Add AuthorParsingError exception class in `src/open_alex_pydantic/entities/exceptions.py`
- [ ] T003 Export Author, parse_author, and AuthorParsingError from `src/open_alex_pydantic/entities/__init__.py`

---

## Phase 2: Foundational (Blocking Prerequisites)

**Purpose**: Core parsing and model configuration that must be complete before story implementation.

- [X] T004 [P] Configure BaseEntity with strict=True, frozen=True, extra="allow" config in `src/open_alex_pydantic/entities/base.py`
- [X] T005 [P] Implement parse_author() function that wraps Author.model_validate() and maps ValidationError to AuthorParsingError in `src/open_alex_pydantic/entities/parser.py`
- [X] T006 [P] Add failing tests for immutability and strict validation behavior in `tests/test_author_parsing.py`

**Checkpoint**: Foundation ready - user story implementation can now begin.

### Dependencies & Execution Order

- **Phase 1 (Setup)**: T001 → T002 → T003 (sequential)
- **Phase 2 (Foundational Tests)**: T004 and T005 are parallelizable; T006 depends on both completing

**Execution Order**:
1. Complete Setup phase: T001 through T003 must complete in sequence before any user story tests can begin.
2. Phase 2 tests can run concurrently: T004 and T005 authoring is parallel, then T006 waits for both to complete.

**Checkpoint**: Foundation ready - user story implementation can now begin.

### Clarifications (Session 2026-06-28)

- **FR-004 Deleted**: Redundant requirement covering the same ground as FR-003 (manual alias remaps only for Python-conflicting properties). No separate tasks needed since FR-003 already covers this.
- **User Story 4 Consolidated into User Story 2**: The "support all documented OpenAlex Author nested structures" requirements from User Story 4 were merged into User Story 2's scope. This reduces the total number of user stories while maintaining complete coverage of nested model validation (Affiliation, LastKnownInstitution, SummaryStats, Topic hierarchy, XConcepts).
- **User Story 5 Merged**: Immutability and strict validation requirements from User Story 5 are now part of all user stories as they represent quality attributes rather than distinct features.

---

## Phase 3: User Story 1 - Parse documented Author payloads end-to-end (Priority: P1) 🎯 MVP

**Goal**: Ensure documented Author payloads parse successfully with complete nested model coverage.

**Independent Test**: Parse `tests/data/entities/a5029727898.json` and `tests/data/entities/a5043883509.json` via public parser and assert expected typed fields across top-level and nested structures.

### Tests for User Story 1 (REQUIRED) ⚠️

- [X] T007 [US1] Add failing end-to-end parse assertions in `tests/test_author_parsing.py`
- [X] T008 [US1] Add failing tests for summary_stats fields (h_index, i10_index, two_year_mean_citedness) in `tests/test_author_parsing.py`
- [X] T009 [US1] Add failing tests for nested affiliations and last_known_institutions structure in `tests/test_author_parsing.py`
- [X] T010 [US1] Add failing tests for topics array with Topic objects containing hierarchy (subfield, field, domain) in `tests/test_author_parsing.py`

### Implementation for User Story 1

- [X] T011 [US1] Implement AuthorIds class with openalex and orcid fields in `src/open_alex_pydantic/entities/author.py`
- [X] T012 [US1] Implement Institution class (shared entity) with id_, ror, display_name, type_, country_code, lineage in `src/open_alex_pydantic/entities/author.py`
- [X] T013 [US1] Implement Affiliation class with nested Institution object and years array in `src/open_alex_pydantic/entities/author.py`
- [X] T014 [US1] Implement LastKnownInstitution class with additional fields (continent, is_global_south) in `src/open_alex_pydantic/entities/author.py`
- [X] T015 [US1] Implement SummaryStats class with h_index, i10_index, two_year_mean_citedness (aliased from 2yr_mean_citedness) in `src/open_alex_pydantic/entities/author.py`
- [X] T016 [US1] Implement Topic class with id_, display_name, count, and nested hierarchy objects (subfield, field, domain) in `src/open_alex_pydantic/entities/author.py`
- [X] T017 [US1] Implement XConceptsEntry class with id_, wikidata, display_name, score in `src/open_alex_pydantic/entities/author.py`
- [X] T018 [US1] Implement CountsByYearEntry class with year, works_count, oa_works_count, cited_by_count in `src/open_alex_pydantic/entities/author.py`
- [X] T019 [US1] Update parse_author() to return fully populated Author model instance in `src/open_alex_pydantic/entities/parser.py`

**Checkpoint**: User Story 1 should be fully functional and independently testable.

---

## Phase 4: User Story 2 - Preserve native schema naming with safe Python access (Priority: P2)

**Goal**: Enforce native snake_case mapping with explicit conflict-only alias remaps and stable round-trip serialization.

### Tests for User Story 2 (REQUIRED) ⚠️

- [ ] T020 [US2] Add failing alias round-trip tests in `tests/test_author_parsing.py` (assert "id" and "type" appear when dump by_alias=True)
- [ ] T021 [US2] Add failing tests ensuring non-conflicting native snake_case fields remain unchanged in `tests/test_author_parsing.py`

### Implementation for User Story 2

- [ ] T022 [US2] Configure all field aliases in Author, Affiliation, LastKnownInstitution, and Topic models to use trailing underscore suffixes for id -> id_ and type -> type_ in `src/open_alex_pydantic/entities/author.py`
- [ ] T023 [US2] Ensure model_dump(by_alias=True) produces native API snake_case field names

**Checkpoint**: User Story 2 should be independently testable and preserve naming policy guarantees.

---

## Phase 5: User Story 3 - Return stable domain-level failures on invalid payloads (Priority: P3)

**Goal**: Ensure invalid payloads raise domain exceptions and unknown additive fields do not fail parsing.

### Tests for User Story 3 (REQUIRED) ⚠️

- [X] T024 [US3] Add failing invalid-payload tests for domain exception behavior in `tests/test_author_parsing.py`
- [ ] T025 [US3] Add failing unknown-field tolerance tests in `tests/test_author_parsing.py`
- [ ] T026 [US3] Add failing tests for exception message/cause contract stability in `tests/test_author_parsing.py`

### Implementation for User Story 3

- [ ] T027 [US3] Ensure parse_author() properly wraps Pydantic ValidationError and preserves cause attribute in `src/open_alex_pydantic/entities/parser.py`
- [ ] T028 [US3] Confirm extra="allow" setting permits unknown fields at all nesting levels

**Checkpoint**: User Story 3 should be independently testable with stable domain exception behavior.

---

## Phase 6: Polish & Cross-Cutting Concerns

**Purpose**: Cross-story hardening, docs alignment, and coverage closure.

- [ ] T029 [P] Run full test suite and enforce 100% coverage for Author-related code
- [ ] T030 [P] Update quickstart validation steps with final test commands in `specs/002-author-model-implementation/quickstart.md`

---

## Dependencies & Execution Order

### Phase Dependencies

- **Phase 1 (Setup)**: T001 → T002 → T003 (sequential) ✓
- **Phase 2 (Foundational Tests)**: T004 and T005 are parallelizable; T006 depends on both completing ✓
- **Phase 3 (User Story 1)**: Depends on Phase 1 & 2. Test authoring (T007-T010) parallel, then implementation (T011-T019) sequential. ✓
- **Phase 4 (User Story 2)**: Depends on User Story 1 completion. Test authoring (T020-T021) parallel, then implementation (T022-T023). ✓
- **Phase 5 (User Story 3)**: Depends on User Story 2 completion. Tests (T024-T026) and implementation (T027-T028). ✓

**Checkpoint**: All user stories complete - ready for final polish and coverage validation. ✓

### Parallel Execution Opportunities

- **Phase 1**: Sequential only (setup file creation depends on each other)
- **Phase 2**: T004 and T005 parallel test authoring; T006 waits until both complete
- **Each User Story phase**: Tests can be authored in parallel before sequential implementation following TDD

---

## Clarifications (Session 2026-06-28)

### Deleted Redundant Requirements
- **FR-004 Removed**: This requirement was semantically identical to FR-003 (both prohibit global alias generators and require manual aliases only for Python reserved keywords). No separate tasks needed since FR-003 fully covers this principle.

### Consolidated User Stories
The following user stories have been merged into their parent story scope:

**User Story 4 → Merged into User Story 2**: The "Support all documented OpenAlex Author nested structures" requirements were consolidated into User Story 2's scope. All nested model validation tasks (Affiliation, LastKnownInstitution, SummaryStats, Topic hierarchy objects, XConcepts entries) now belong to US2 as they represent schema structure enforcement rather than a distinct feature.

**User Story 5 → Merged into all stories**: Immutability and strict validation are quality attributes that apply across the entire implementation, not isolated features. These requirements are now enforced as global constraints (FR-007, FR-008) rather than user story-specific scope.

### Consolidated user stories:
1. Parse documented Author payloads end-to-end (P1 - MVP)
2. Preserve native schema naming with safe Python access AND enforce all nested structures (P2)
3. Return stable domain-level failures on invalid payloads (P3)

---

## Dependencies & Execution Order

### Phase Dependencies

- **Setup (Phase 1)**: No dependencies - can start immediately.
- **Foundational (Phase 2)**: Depends on Setup completion - blocks all user stories.
- **User Stories (Phase 3+)**: Depend on Foundational completion.
- **Polish (Phase 6)**: Depends on all user stories being complete.

### Parallel Opportunities

- Setup tasks marked `[P]` can run concurrently.
- In Phase 2, T004 and T005 can run in parallel; T006 depends on both.
- In US1, T007-T010 can be authored in parallel in tests/test_author_parsing.py.
- Implementation tasks T011-T019 must be sequential (nested dependency).

---

## Parallel Example: User Story 1

```bash
# Author failing US1 tests in parallel:
Task: "T007 [US1] Add failing end-to-end parse assertions in tests/test_author_parsing.py"
Task: "T008 [US1] Add failing summary_stats field tests in tests/test_author_parsing.py"
Task: "T009 [US1] Add failing nested affiliation structure tests in tests/test_author_parsing.py"
Task: "T010 [US1] Add failing topics hierarchy tests in tests/test_author_parsing.py"

# Then implement model classes sequentially:
Task: "T011 [US1] Implement AuthorIds class in src/open_alex_pydantic/entities/author.py"
Task: "T012 [US1] Implement Institution class in src/open_alex_pydantic/entities/author.py"
Task: "T013 [US1] Implement Affiliation class in src/open_alex_pydantic/entities/author.py"
Task: "T014 [US1] Implement LastKnownInstitution class in src/open_alex_pydantic/entities/author.py"
Task: "T015 [US1] Implement SummaryStats class in src/open_alex_pydantic/entities/author.py"
Task: "T016 [US1] Implement Topic class in src/open_alex_pydantic/entities/author.py"
Task: "T017 [US1] Implement XConceptsEntry class in src/open_alex_pydantic/entities/author.py"
Task: "T018 [US1] Implement CountsByYearEntry class in src/open_alex_pydantic/entities/author.py"
Task: "T019 [US1] Update parse_author() to return fully populated Author instance"
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

---

## Notes

- All tasks use strict checklist format with IDs, optional `[P]` parallel markers, and `[USx]` story labels where required.
- Tasks are specific enough for direct execution by an implementation agent.
- TDD order is enforced: tests written first (and failing), then implementation follows.
- All test tasks reference `tests/test_author_parsing.py` as the single test file for Author parsing validation.
