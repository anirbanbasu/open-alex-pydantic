# Feature Specification: Author Model Implementation

**Feature Branch**: `[002-author-model-implementation]`

**Created**: 2026-06-28

**Status**: Specified

**Plan**: `specs/002-author-model-implementation/plan.md`

**Input**: User description: "Extend the specification to implement the Author model with specs written to specs/002-author-model-implementation as the second phase. Use the OpenAlex API specifications for authors at https://developers.openalex.org/api-reference/authors.md to create the necessary specification."

## User Scenarios & Testing *(mandatory)*

### User Story 1 - Parse documented Author payloads end-to-end (Priority: P1)

As a library consumer, I want Author API responses to parse into a complete Author model (including all nested objects and arrays) so I can rely on validated structured data for downstream analysis of author profiles, their works count, citations, institutions, and topic classifications.

**Why this priority**: This is the foundational contract for author-centric analysis across the OpenAlex ecosystem and enables rich bibliometric insights.

**Independent Test**: Can be fully tested by parsing representative OpenAlex Author payload fixtures (minimal with only required fields and rich with all optional nested objects) and asserting successful model creation with expected values.

**Acceptance Scenarios**:

1. **Given** a valid Author payload containing documented top-level fields (id, display_name, orcid), summary stats (h_index, i10_index, 2yr_mean_citedness), affiliations array, last_known_institutions array, and topics array, **When** it is parsed, **Then** an Author model is created with all mapped fields available at the appropriate nesting levels including nested objects and arrays.

2. **Given** a valid Author payload where optional documented fields are absent or null (scopus, parsed_longest_name, x_concepts), **When** it is parsed, **Then** parsing succeeds and missing optional fields are represented as null-equivalent model values (None for single fields, empty lists [] for arrays).

3. **Given** a valid Author payload with works_count and cited_by_count populated at the author level, **When** it is parsed, **Then** these metrics are available as simple integer fields on the root Author model instance.

---

### User Story 2 - Preserve native schema naming while handling reserved Python keywords (Priority: P2)

As a developer using the model, I want API-native snake_case fields preserved except for reserved Python keywords safely exposed, so I can work with both API fidelity and valid Python syntax without conflicts or NameError exceptions.

**Why this priority**: Reserved keyword conflicts in Python cause immediate runtime errors that are difficult to diagnose (as_id, as_type, license would shadow built-ins).

**Independent Test**: Can be tested by parsing payloads containing reserved naming patterns and asserting only approved remaps for Python's `id` and `type` keywords are used with trailing-underscore suffixes.

**Acceptance Scenarios**:

1. **Given** a payload containing the documented id field (OpenAlex ID), **When** it is parsed, **Then** the value is available through the id_ field (with underscore suffix) since `id` is a Python keyword, while all other non-conflicting snake_case fields from the API retain their native names.

2. **Given** a payload containing the documented type field (institution type), **When** it is parsed, **Then** the value is available through the type_ field (with underscore suffix) since `type` is a Python keyword built-in function.

3. **Given** a payload with other non-conflicting native snake_case fields such as display_name, orcid, scopus, summary_stats, h_index, i10_index, works_count, cited_by_count, from_created_date, to_created_date, and to_updated_date, **When** it is parsed, **Then** these field names remain unchanged with no global alias rewrite behavior.

4. **Given** a payload containing arrays of affiliated institutions with type_ fields in each nested object, **When** it is parsed, **Then** the array includes proper Affiliation models where reserved keywords are aliased appropriately without breaking JSON deserialization.

---

### User Story 3 - Return stable domain-level failures on invalid payloads (Priority: P3)

As an integrator, I want invalid Author payloads to fail with project domain exceptions instead of third-party validation errors, so application error handling remains stable and provides meaningful messages about what was wrong with the author data.

**Why this priority**: Stable, package-defined error contracts reduce coupling to validation internals and allow consistent error handling across the application.

**Independent Test**: Can be tested by feeding invalid payloads to public parsing entry points and asserting raised exception types and messages are package-defined (not raw Pydantic model validation exceptions).

**Acceptance Scenarios**:

1. **Given** an invalid payload with wrong data types in required nested structures (e.g., summary_stats as a string instead of object, or id not matching OpenAlex ID pattern), **When** parsed through public interfaces, **Then** parsing fails with domain exceptions that clearly describe the validation error (e.g., ValidationError with message indicating "summary_stats must be an object containing h_index, i10_index, and 2yr_mean_citedness") rather than raw Pydantic model_revalidate exception internals.

2. **Given** a payload with extra undocumented fields at the top level or within nested objects (affiliations, last_known_institutions), **When** parsed through public interfaces, **Then** parsing behavior remains graceful using pydantic.v1.Extra.allow mode and does not fail validation solely due to those properties; unknown properties MAY be retained as extra data but MUST NOT alter validation outcomes for represented fields.

3. **Given** an author payload with malformed nested objects in affiliations (missing required id or type fields), **When** parsed, **Then** parsing fails with clear domain exceptions indicating which nested object failed validation and why (e.g., "Affiliation requires id field" or "Affiliation requires type field").

---

### User Story 4 - Support all documented OpenAlex Author nested structures (Priority: P2)

As a data consumer performing bibliometric analysis, I want the Author model to fully represent the complex nested schema of the OpenAlex author entity so I can access citation metrics, institutional history, topic classifications, and any additional concept indexing.

**Why this priority**: The richness of the nested structures is what makes author records useful for analytics; omitting them fundamentally breaks the use case.

**Independent Test**: Can be tested by asserting that each documented nested structure type (Affiliation, LastKnownInstitution, SummaryStats, ParsedLongestName, XConcepts, Topic) can be instantiated as a model class and accessed via its corresponding array field.

**Acceptance Scenarios**:

1. **Given** a payload with affiliations array containing objects with id, type, ror, country_code fields, **When** parsed, **Then** the result includes an affiliations attribute that is a list of Affiliation models matching the schema structure from the API.

2. **Given** a payload with last_known_institutions array containing objects with id, type, ror, country_code, continent, lineage, and is_global_south fields, **When** parsed, **Then** the result includes a last_known_institutions attribute that is a list of LastKnownInstitution models (structured identically to Affiliation but including additional documented fields).

3. **Given** a payload with summary_stats object containing h_index, i10_index, and 2yr_mean_citedness fields, **When** parsed, **Then** the result includes a summary_stats attribute that is a SummaryStats model (not just raw dict) exposing these metrics as typed properties.

4. **Given** a payload with parsed_longest_name object containing first, last, middle, and suffix fields, **When** parsed, **Then** the result includes a parsed_longest_name attribute that is a ParsedLongestName model exposing name components separately.

5. **Given** a payload with x_concepts array (for concept indexing via x-headers), **When** parsed, **Then** the result includes an x_concepts attribute that is a list of simple objects or Concept models as specified by the API schema.

6. **Given** a payload with topics array containing topic objects with id fields, **When** parsed, **Then** the result includes a topics attribute that is a list of Topic models matching the API topic schema.

---

### User Story 5 - Model immutability and strict validation (Priority: P2)

As a library maintainer, I want Author model instances to be immutable and validation to be strict so downstream consumers can safely use parsed author data without worrying about unexpected mutations or type coercion surprises.

**Why this priority**: Immutability guarantees data integrity for analytics pipelines; strict validation prevents silent type conversion bugs in dependent code.

**Independent Test**: Can be tested by attempting to modify model instances (expecting errors) and passing strict mode validation with incompatible types.

**Acceptance Scenarios**:

1. **Given** an Author instance successfully parsed from a valid payload, **When** an attempt is made to mutate any field (display_name, id_, summary_stats fields, array elements), **Then** the operation fails with an immutability error (FrozenInstanceError or similar) indicating the model cannot be modified.

2. **Given** an Author instance parsed from valid data, **When** it is used in a downstream application that modifies nested objects or reassigns fields, **Then** modifications are blocked and the original data remains intact (frozen config propagates to nested models).

3. **Given** parsing input with mismatched types (e.g., h_index as string "45" instead of integer 45), **When** validation runs in strict mode, **Then** parsing fails immediately without attempting to coerce the incompatible value.

---

## Requirements *(mandatory)*

### Functional Requirements

- **FR-001**: System MUST provide an Author model that represents documented Author schema sections including id, display_name, orcid, scopus, summary_stats (with h_index, i10_index, 2yr_mean_citedness), affiliations (array of Affiliation objects with id, type, ror, country_code, lineage), last_known_institutions (array of LastKnownInstitution objects with additional fields including continent and is_global_south), parsed_longest_name (with first, last, middle, suffix), x_concepts (array), topics (array of Topic objects with id), from_created_date, to_created_date, to_updated_date, works_count, cited_by_count, and block_key.

- **FR-002**: System MUST parse valid Author payloads containing documented top-level and nested fields such that represented fields are preserved exactly for value and structure; this includes:
  - Top-level fields: id (aliased to id_), display_name, orcid, scopus, block_key, works_count, cited_by_count, from_created_date, to_created_date, to_updated_date
  - Summary stats object: h_index, i10_index, 2yr_mean_citedness as typed integer/float properties accessible via summary_stats attribute
  - Arrays: affiliations and last_known_institutions as lists of nested institution model objects; topics as list of Topic objects; x_concepts as array (may be empty)

- **FR-003**: System MUST use manual alias remaps only for Python-conflicting API properties documented in the Author schema: id -> id_ (since `id` is a Python keyword), type -> type_ (since `type` is a built-in function in Python).

- **FR-005**: System MUST define nested model structures for:
  - SummaryStats: h_index (integer), i10_index (integer), 2yr_mean_citedness (float)
  - Affiliation: id, type, ror, country_code, lineage (optional)
  - LastKnownInstitution: id, type, ror, country_code, continent, lineage (optional), is_global_south (boolean)
  - ParsedLongestName: first, last, middle (optional), suffix (optional)
  - XConcepts: id (string reference)
  - Topic: id (string reference)

- **FR-006**: System MUST NOT implement model inheritance patterns that would allow dehydrated objects to expand; instead parse documented structures directly or represent as strings/dicts when payloads are dehydrated.

- **FR-007**: System MUST enforce immutable model instances for Author and all nested model structures within this feature scope (frozen=True configuration).

- **FR-008**: System MUST apply strict validation so incompatible input types are rejected instead of silently coerced (strict=True in Pydantic).

- **FR-009**: System MUST accept payloads containing additive unknown properties at any nesting level without failing validation solely due to those properties; pydantic.v1.Extra.allow mode must be used to permit extra fields while only validating documented fields.

- **FR-010**: System MUST expose public parsing entry points that map validation failures to project-defined domain exceptions (e.g., ValidationError with descriptive message) rather than raw Pydantic model_validate_exceptions outputs.

- **FR-011**: System MUST include test coverage that validates all added and modified behavior for Author parsing, aliasing, immutability, strict validation, unknown-field handling, nested object structures, array handling, and domain exception mapping.

---

### Quality and Validation Requirements *(mandatory)*

- **QV-001**: Feature tests MUST be authored first and demonstrated failing before implementation (tests-driven development).

- **QV-002**: New and modified code MUST maintain 100% test coverage for all public fields, nested structures, validation paths, and error conditions.

- **QV-003**: Python code MUST use explicit type hints compatible with Python 3.12+ (type annotations from typing module for complex types like Dict, List, Optional).

- **QV-004**: Pydantic v2 models MUST run with strict validation enabled and immutable frozen configuration; nested models must also be frozen to prevent mutation through the parent Author instance.

- **QV-005**: Models MUST map directly to native snake_case API fields with no global alias generators; manual aliases are allowed only for reserved/built-in remaps (id -> id_, type -> type_). The schema structure from the OpenAlex API must be preserved in model definitions.

- **QV-006**: Public parsing interfaces MUST map validation failures to domain exceptions with meaningful error messages that help developers understand what went wrong with their payload.

- **QV-007**: All nested objects (SummaryStats, Affiliation, LastKnownInstitution, ParsedLongestName, Topic) and arrays (affiliations, last_known_institutions, x_concepts, topics) MUST be validated as model structures when present in payloads.

---

## Success Criteria *(mandatory)*

### Measurable Outcomes

- **SC-001**: 100% of curated valid Author fixtures (minimal with only required fields, typical with common optional data, and rich with all nested objects) parse successfully through public model parsing interfaces.

- **SC-002**: 100% of curated invalid Author fixtures that violate declared field types or structure fail with domain exceptions rather than raw validation-library exceptions.

- **SC-003**: 100% of documented API fields (id, display_name, orcid, scopus, works_count, cited_by_count, from_created_date, to_created_date, to_updated_date, summary_stats, affiliations, last_known_institutions, parsed_longest_name, x_concepts, topics, block_key) are represented in the Author model either as direct attributes or nested structures with correct Python naming (id_ and type_ aliased).

- **SC-004**: 100% of tested reserved-name API properties (id field, type field) use trailing-underscore aliases to avoid Python keyword conflicts.

- **SC-005**: summary_stats object fields (h_index, i10_index, two_year_mean_citedness aliased from 2yr_mean_citedness) are accessible as typed integer/float properties on the Author instance via the nested summary_stats attribute.

- **SC-006**: affiliations array contains valid Affiliation model objects when populated in payloads; empty arrays parse successfully.

- **SC-007**: last_known_institutions array contains valid LastKnownInstitution model objects when populated; distinguishes from affiliations by additional fields (continent, is_global_south).

- **SC-008**: parsed_longest_name object fields are accessible as typed properties on the Author instance when present in payload.

- **SC-009**: topics array contains valid Topic model objects when populated in payloads; empty arrays parse successfully.

- **SC-010**: x_concepts array (for concept indexing) parses as an empty list or valid entries when present; missing field defaults to empty list.

- **SC-011**: Attempting to mutate any Author instance or nested object fails with immutability error.

- **SC-012**: Passing incompatible types to model validation fails strictly without coercion (e.g., string "45" for h_index rejects instead of coercing to 45).

---

## Assumptions

- The OpenAlex Authors documentation at https://developers.openalex.org/api-reference/authors.md is the baseline contract for this feature scope.
- Author model should use Pydantic v2 with pydantic.v1.Extra.allow mode (consistent with Work model specification) to permit extra fields in payloads while validating documented fields.
- Nested structures are parsed as Pydantic models when present; if payloads contain dehydrated objects (with _id and __schema keys), they remain as string/dict references.
- The summary_stats structure (h_index, i10_index, 2yr_mean_citedness) is a nested object in the author schema (not an array like some other fields).
- Date fields follow ISO 8601 format (YYYY-MM-DD strings for from_created_date, to_created_date, to_updated_date).
- Array structures include: affiliations[], last_known_institutions[], x_concepts[], topics[].
