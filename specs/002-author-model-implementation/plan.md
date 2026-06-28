# Implementation Plan: Author Model

**Created**: 2026-06-28

**Input**: Specification from `specs/002-author-model-implementation/spec.md`

**Tests**: Test tasks are REQUIRED. Follow strict TDD and maintain 100% coverage for all new and modified code.

---

## Technical Context

Based on the Author model specification and OpenAlex API requirements:

### Known Requirements (from spec.md)

1. **Nested Structures Required**:
    - `AuthorIds` - External identifiers (openalex, orcid)
    - `Institution` - Shared entity for affiliation institutions with id_, ror, display_name, type_, country_code, lineage
    - `Affiliation` - Author affiliation with nested Institution object and years array
    - `LastKnownInstitution` - Last known institutions with additional fields (continent, is_global_south)
    - `SummaryStats` - Citation metrics (h_index, i10_index, 2yr_mean_citedness -> two_year_mean_citedness)
    - `Topic` - Topic classifications with hierarchy (subfield, field, domain)
    - `TopicHierarchyEntry` - Reference entity for topic hierarchies
    - `XConceptsEntry` - X-headers concept entries with score
    - `CountsByYearEntry` - Yearly publication counts

2. **Python Keyword Aliases Required**:
    - `id` -> `id_` (Python reserved keyword)
    - `type` -> `type_` (built-in function)
    - `2yr_mean_citedness` -> `two_year_mean_citedness` (invalid Python identifier, uses underscore prefix in alias)

3. **Model Configuration Requirements**:
    - Strict validation enabled
    - Immutable (frozen=True)
    - Extra fields allowed (extra="allow") for forward compatibility

4. **Error Handling**:
    - Public parsing boundary must map Pydantic ValidationError to domain exceptions
    - AuthorParsingError exception class required

### NEEDS CLARIFICATION: None - All requirements are clear from the OpenAlex API specification

---

## Constitution Check

✅ **TDD Gate** - Test files exist and tests will be authored first.

✅ **Strict Typing** - Python 3.12+ compatible with explicit type hints.

✅ **Immutable Native-Schema Model Design** - Models will inherit frozen configuration from BaseEntity; manual aliases only for reserved/built-in conflicts (id_, type_, two_year_mean_citedness).

✅ **Defensive Parsing** - Unknown fields tolerated via extra="allow"; validation failures mapped to domain exceptions.

✅ **Compatibility** - Conservative evolution of public API; breaking changes documented.

---

## Phase 1: Setup (Shared Infrastructure)

**Purpose**: Prepare fixture and test scaffolding for strict TDD execution.

- [ ] T001 Create Author model source file at `src/open_alex_pydantic/entities/author.py` with all nested entity classes (AuthorIds, Institution, Affiliation, LastKnownInstitution, SummaryStats, TopicHierarchyEntry, Topic, XConceptsEntry, CountsByYearEntry)
- [ ] T002 Add AuthorParsingError exception class in `src/open_alex_pydantic/entities/exceptions.py`
- [ ] T003 Export Author, parse_author, and AuthorParsingError from `src/open_alex_pydantic/entities/__init__.py`

---

## Phase 2: Foundational (Blocking Prerequisites)

**Purpose**: Core parsing and model configuration that must be complete before story implementation.

- [ ] T004 Configure BaseEntity with strict=True, frozen=True, extra="allow" config in `src/open_alex_pydantic/entities/base.py`
- [ ] T005 Implement parse_author() function that wraps Author.model_validate() and maps ValidationError to AuthorParsingError in `src/open_alex_pydantic/entities/parser.py`
- [ ] T006 Add failing tests for immutability and strict validation behavior in `tests/test_author_parsing.py`

**Checkpoint**: Foundation ready - user story implementation can now begin.

### Dependencies & Execution Order

- **Phase 1 (Setup)**: T001 → T002 → T003 (sequential)
- **Phase 2 (Foundational Tests)**: T004 and T005 are parallelizable; T006 depends on both completing

**Execution Order**:
1. Complete Setup phase: T001 through T003 must complete in sequence before any user story tests can begin.
2. Phase 2 tests can run concurrently: T004 and T005 authoring is parallel, then T006 waits for both to complete.

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

## Phase 3: User Story 1 - Parse documented Author payloads end-to-end (Priority: P1) 🎯 MVP

**Goal**: Ensure documented Author payloads parse successfully with complete nested model coverage.

**Independent Test**: Parse `tests/data/entities/a5029727898.json` and `tests/data/entities/a5043883509.json` via public parser and assert expected typed fields across top-level and nested structures.

### Tests for User Story 1 (REQUIRED) ⚠️

- [ ] T007 Add failing end-to-end parse assertions in `tests/test_author_parsing.py`
- [ ] T008 Add failing tests for summary_stats fields (h_index, i10_index, two_year_mean_citedness) in `tests/test_author_parsing.py`
- [ ] T009 Add failing tests for nested affiliations and last_known_institutions structure in `tests/test_author_parsing.py`
- [ ] T010 Add failing tests for topics array with Topic objects containing hierarchy (subfield, field, domain) in `tests/test_author_parsing.py`

### Implementation for User Story 1

- [ ] T011 Implement AuthorIds class with openalex and orcid fields in `src/open_alex_pydantic/entities/author.py`
- [ ] T012 Implement Institution class (shared entity) with id_, ror, display_name, type_, country_code, lineage in `src/open_alex_pydantic/entities/author.py`
- [ ] T013 Implement Affiliation class with nested Institution object and years array in `src/open_alex_pydantic/entities/author.py`
- [ ] T014 Implement LastKnownInstitution class with additional fields (continent, is_global_south) in `src/open_alex_pydantic/entities/author.py`
- [ ] T015 Implement SummaryStats class with h_index, i10_index, two_year_mean_citedness (aliased from 2yr_mean_citedness) in `src/open_alex_pydantic/entities/author.py`
- [ ] T016 Implement Topic class with id_, display_name, count, and nested hierarchy objects (subfield, field, domain) in `src/open_alex_pydantic/entities/author.py`
- [ ] T017 Implement XConceptsEntry class with id_, wikidata, display_name, score in `src/open_alex_pydantic/entities/author.py`
- [ ] T018 Implement CountsByYearEntry class with year, works_count, oa_works_count, cited_by_count in `src/open_alex_pydantic/entities/author.py`
- [ ] T019 Update parse_author() to return fully populated Author model instance in `src/open_alex_pydantic/entities/parser.py`

**Checkpoint**: User Story 1 should be fully functional and independently testable.

---

## Phase 4: User Story 2 - Preserve native schema naming with safe Python access AND enforce all nested structures (Priority: P2)

**Goal**: Enforce native snake_case mapping with explicit conflict-only alias remaps, stable round-trip serialization, and validate all nested OpenAlex API structures.

### Tests for User Story 2 (REQUIRED) ⚠️

- [ ] T020 Add failing alias round-trip tests in `tests/test_author_parsing.py` (assert "id" and "type" appear when dump by_alias=True)
- [ ] T021 Add failing tests ensuring non-conflicting native snake_case fields remain unchanged in `tests/test_author_parsing.py`

### Implementation for User Story 2

- [ ] T022 Configure all field aliases in Author, Affiliation, LastKnownInstitution, and Topic models to use trailing underscore suffixes for id -> id_ and type -> type_ in `src/open_alex_pydantic/entities/author.py`
- [ ] T023 Ensure model_dump(by_alias=True) produces native API snake_case field names

**Checkpoint**: User Story 2 should be independently testable and preserve naming policy guarantees.

---

## Phase 5: User Story 3 - Return stable domain-level failures on invalid payloads (Priority: P3)

**Goal**: Ensure invalid payloads raise domain exceptions and unknown additive fields do not fail parsing.

### Tests for User Story 3 (REQUIRED) ⚠️

- [ ] T024 Add failing invalid-payload tests for domain exception behavior in `tests/test_author_parsing.py`
- [ ] T025 Add failing unknown-field tolerance tests in `tests/test_author_parsing.py`
- [ ] T026 Add failing tests for exception message/cause contract stability in `tests/test_author_parsing.py`

### Implementation for User Story 3

- [ ] T027 Ensure parse_author() properly wraps Pydantic ValidationError and preserves cause attribute in `src/open_alex_pydantic/entities/parser.py`
- [ ] T028 Confirm extra="allow" setting permits unknown fields at all nesting levels

**Checkpoint**: User Story 3 should be independently testable with stable domain exception behavior.

---

## Phase 6: Polish & Cross-Cutting Concerns

**Purpose**: Cross-story hardening, docs alignment, and coverage closure.

- [ ] T029 Run full test suite and enforce 100% coverage for Author-related code
- [ ] T030 Update quickstart validation steps with final test commands in `specs/002-author-model-implementation/quickstart.md`

---

## Dependencies & Execution Order

### Phase Dependencies

- **Setup (Phase 1)**: No dependencies - can start immediately. T001-T003 must complete in sequence.
- **Foundational (Phase 2)**: Depends on Setup completion - blocks all user stories. T004-T005 are parallelizable; T006 depends on both.
- **User Story 1 (Phase 3)**: Depends on Foundational completion. Tests first (T007-T010), then implementation (T011-T019).
- **User Story 2 (Phase 4)**: Depends on User Story 1 completion and Setup+Foundational phases.
- **User Story 3 (Phase 5)**: Depends on User Story 2 completion and all previous phases.
- **Polish (Phase 6)**: Depends on all user stories being complete.

### Parallel Opportunities

- **Setup tasks**: T001, T002, T003 must execute sequentially (setup files depend on each other).
- **Phase 2 tests**: T004 and T005 can run in parallel; T006 blocked until both complete.
- **Within User Story phases**: Test tasks can be authored in parallel while implementation follows TDD ordering.

---

## Notes

- All tasks use strict checklist format with IDs, optional `[P]` parallel markers (where genuinely parallelizable), and `[USx]` story labels where required.
- Tasks are specific enough for direct execution by an implementation agent.
- TDD order is enforced: tests written first (and failing), then implementation follows.
- User stories were consolidated from 5 to 3 based on quality attribute consolidation (immutability and strict validation as global constraints).
- Redundant FR-004 requirement was removed due to semantic duplication with FR-003.
