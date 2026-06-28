# Specification Quality Checklist: Author Model Implementation

**Purpose**: Validate specification completeness and quality before proceeding to implementation planning
**Created**: 2026-06-28
**Feature**: `specs/002-author-model-implementation/spec.md`

## Requirement Completeness (Are all necessary requirements documented?)

- [ ] CHK001 - Are all documented OpenAlex Author API fields represented in the model hierarchy? [Completeness, Spec §FR-001]
  - **Validation**: Verify FR-001 lists: id, display_name, orcid, scopus, summary_stats, affiliations, last_known_institutions, parsed_longest_name, x_concepts, topics, ids, works_count, cited_by_count, and block_key. All fields present.

- [ ] CHK002 - Are nested structures (SummaryStats, Affiliation, LastKnownInstitution, Topic, ParsedLongestName) explicitly defined with their own model classes? [Completeness, Spec §FR-005]
  - **Validation**: FR-005 enumerates five nested model requirements with exact field lists. All structures documented including hierarchy entry types (subfield, field, domain).

- [ ] CHK003 - Are array/list fields properly enumerated as distinct data structures in requirements? [Completeness, Spec §FR-002]
  - **Validation**: FR-002 specifies affiliations and last_known_institutions as lists of nested objects, topics as list of Topic objects, x_concepts as array. All arrays accounted for with proper typing.

- [ ] CHK004 - Are the six test scenarios from User Story 1 through User Story 5 fully enumerated in requirements? [Completeness, Spec §User Stories]
  - **Validation**: US1 has 3 acceptance scenarios, US2 has 4 scenarios, US3 has 3 scenarios, US4 has 6 scenarios, US5 has 3 scenarios. All documented and testable.

- [ ] CHK005 - Is the shared Institution entity requirement explicitly documented (avoiding duplication between Affiliation and LastKnownInstitution)? [Completeness, Spec §FR-005]
  - **Validation**: FR-005 notes Institution as "shared entity for affiliation institutions". However, this could be clarified: should Affiliation and LastKnownInstitution both reference a shared Institution model, or be independent structures?

- [ ] CHK006 - Are date fields (from_created_date, to_created_date, to_updated_date) documented with validation rules for ISO 8601 format? [Completeness, Spec §FR-002]
  - **Validation**: Assumions section mentions "Date fields follow ISO 8601 format" but FR-002 does not explicitly include these date fields. Consider adding explicit field documentation in FR-001 or FR-002.

- [ ] CHK007 - Are all x-concept index fields (wikidata, display_name, score) documented in requirements for the XConceptsEntry model? [Completeness, Spec §FR-005]
  - **Validation**: Assumptions section lists "x_concepts array" but FR-005 only mentions "XConcepts: id (string reference)". Consider adding full field specification for XConcepts entry structure.

---

## Requirement Clarity (Are requirements specific and unambiguous?)

- [ ] CHK008 - Is the distinction between "id_" at top level versus "id_" nested within Institution objects clearly differentiated in requirements? [Clarity, Spec §FR-003]
  - **Validation**: FR-003 states `id -> id_` alias and FR-002 references both. However, could be clearer: Top-level `id` becomes `id_`, but nested `id` fields in Institution objects also become `id_`. Consider explicit statement about scoping.

- [ ] CHK009 - Is the "2yr_mean_citedness" alias to "two_year_mean_citedness" clearly justified (not just Python identifier validity)? [Clarity, Spec §FR-005]
  - **Validation**: FR-005 uses `two_year_mean_citedness` as the model field name but does not explain why this naming convention differs from the API's `2yr_` prefix. Consider adding rationale or explicitly stating Python identifier validity requirement.

- [ ] CHK010 - Are the three reserved keyword exceptions (id_, type_, and two_year_mean_citedness) exhaustively listed? [Clarity, Spec §FR-003]
  - **Validation**: FR-003 lists `id -> id_` and `type -> type_`, FR-005 uses `two_year_mean_citedness`. However, the third alias is not explicitly called out as a reserved-name exception. Consider consolidating all aliases in one location.

- [ ] CHK011 - Is "parsed_longest_name" (a string field) clearly distinguished from potential nested name structures? [Clarity, Spec §FR-005]
  - **Validation**: FR-002 mentions `parsed_longest_name` but Assumptions section lists it as a separate parseable object with first/last/middle/suffix fields. Are we validating the string value or a nested structure?

- [ ] CHK012 - Are field type coercions explicitly forbidden in requirements (e.g., "h_index must be integer, not string")? [Clarity, Spec §FR-008]
  - **Validation**: FR-008 states "incompatible input types are rejected" but could be more explicit: e.g., "integer h_index values must not coerce from string representations" given strict=True enforcement.

---

## Requirement Consistency (Do requirements align without conflicts?)

- [ ] CHK013 - Is the Institution model structure consistent between its use in Affiliation and LastKnownInstitution? [Consistency, Spec §FR-005]
  - **Validation**: FR-005 defines Institution once but uses it differently in Affiliation (with `id_`, `type_`, `country_code`) versus LastKnownInstitution (with `id_`, `type_`, `country_code`, plus `continent`, `is_global_south`). Ensure the base fields are properly shared.

- [ ] CHK014 - Are Topic hierarchy entries (subfield, field, domain) documented consistently across all references to topics? [Consistency, Spec §FR-005]
  - **Validation**: FR-005 defines `TopicHierarchyEntry` as a standalone model but FR-002 mentions topics as "list of Topic objects". Clarify whether Topic includes these hierarchy fields or if they're separate nested objects under each Topic.

- [ ] CHK015 - Is the extra-fields behavior consistent across all nested structures (top-level and nested)? [Consistency, Spec §FR-009]
  - **Validation**: FR-009 says "unknown properties MAY be retained as extra data" for top-level fields and nested objects. Verify this applies uniformly to: top-level Author fields, Institution objects in affiliations, Institution objects in last_known_institutions, Topic objects, and XConcepts entries.

---

## Acceptance Criteria Quality (Are success criteria measurable?)

- [ ] CHK016 - Is "100% of curated valid Author fixtures" testable with specific fixture counts or examples? [Measurability, Spec §SC-001]
  - **Validation**: SC-001 uses the term "curated valid Author fixtures" but does not enumerate what constitutes a fixture set. Consider referencing actual file paths (e.g., `a5029727898.json`, `a5043883509.json`) or defining selection criteria.

- [ ] CHK017 - Is "100% of documented API fields" verifiable against a known schema? [Measurability, Spec §SC-003]
  - **Validation**: SC-003 lists all field names explicitly including dates and IDs, making this measurable. Success criterion is objectively testable by checking each named field exists in model definition.

- [ ] CHK018 - Are reserved-name fields (id_ and type_) measurably verifiable for round-trip serialization? [Measurability, Spec §SC-004]
  - **Validation**: SC-004 states "100% of tested reserved-name API properties use trailing-underscore aliases". Combined with alias round-trip test (dump by_alias=True), this is objectively verifiable.

---

## Scenario Coverage (Are all flows/cases addressed?)

- [ ] CHK019 - Is the empty array scenario documented for each array field (affiliations, last_known_institutions, x_concepts, topics)? [Coverage, Spec §User Stories]
  - **Validation**: US1 #2 mentions "empty lists [] for arrays" but no other user story explicitly addresses what happens when these arrays are absent from payloads. Ensure empty/null array handling is covered in FR-002 or FR-009.

- [ ] CHK020 - Are partial/missing nested object scenarios documented (e.g., Institution missing required id field)? [Coverage, Spec §User Story 3 #3]
  - **Validation**: US3 #3 mentions "malformed nested objects in affiliations" but doesn't specify which fields can be missing. Consider clarifying: does extra="allow" permit partial objects or must documented fields all be present?

- [ ] CHK021 - Is the topic hierarchy (subfield, field, domain) scenario sufficiently covered across User Story 4 scenarios? [Coverage, Spec §User Story 4 #6]
  - **Validation**: US4 #6 mentions topics array with id fields but doesn't explicitly cover whether subfield/field/domain nested structures are validated as TopicHierarchyEntry objects. Consider adding explicit requirement for topic object structure.

---

## Edge Case Coverage (Are boundary conditions defined?)

- [ ] CHK022 - Is the dehydrated payload scenario addressed (objects with _id and __schema keys that should not expand)? [Edge Case, Spec §FR-006]
  - **Validation**: FR-006 explicitly forbids expanding dehydrated objects but doesn't specify how to handle them in parsing. Consider adding: "dehydrated payload fields remain as string references without model expansion".

- [ ] CHK023 - Are null/missing optional field scenarios documented for each nullable type? [Edge Case, Spec §FR-009]
  - **Validation**: FR-009 covers unknown additive properties but doesn't explicitly address the difference between "absent fields" and "present null values". Consider clarifying both scenarios.

- [ ] CHK024 - Is the strict validation vs extra-allow tension addressed for nested structures? [Edge Case, Spec §QV-004]
  - **Validation**: QV-004 requires frozen models but FR-009 uses extra="allow". This is not a contradiction (frozen applies to mutation after creation; extra="allow" permits unknown input fields), but the combination could be clarified.

---

## Non-Functional Requirements (Performance, Security, etc.)

- [ ] CHK025 - Is there a performance requirement for parsing large author payloads with many affiliations? [Non-Functional, Gap]
  - **Assessment**: No performance SLA or throughput requirements are documented for Author model operations. Consider adding: "Author model must parse payloads with N affiliated institutions within X ms".

---

## Traceability (Can each requirement be linked to its source?)

- [ ] CHK026 - Is every FR item traceable to the OpenAlex API specification? [Traceability, Spec §FR-*]
  - **Assessment**: All functional requirements can be traced back to https://developers.openalex.org/api-reference/authors.md documentation referenced in User Story 1 "Input" section.

- [ ] CHK027 - Is there a requirement ID scheme established for cross-document referencing? [Traceability, Spec §FR-001]
  - **Validation**: A numbering convention (FR-001 through FR-011, QV-001 through QV-007) is used consistently throughout the document. This enables unambiguous cross-references between requirements sections.

---

## Ambiguities & Conflicts (What needs clarification?)

- [ ] CHK028 - Clarify: Should Affiliation inherit all Institution fields or only a subset? [Ambiguity, Spec §FR-005]
  - **Open Question**: FR-005 defines Affiliation with `id_`, `type_`, `ror`, `country_code`, `lineage` plus an optional nested `institution` object. The structure implies Affiliation wraps Institution rather than being equivalent to it. Verify this design intent is correct.

- [ ] CHK029 - Clarify: Does last_known_institutions differ from affiliations only by additional fields? [Ambiguity, Spec §FR-005]
  - **Open Question**: FR-005 defines both structures with different fields but doesn't explicitly state they should be distinguished this way. Consider documenting: "last_known_institutions = Institution structure extended with continent and is_global_south fields".

- [ ] CHK030 - Clarify: What is the relationship between parsed_longest_name string field and ParsedLongestName nested model? [Ambiguity, Spec §FR-005]
  - **Open Question**: Author has both `parsed_longest_name: Optional[str] = None` (FR-005) and a referenced structure with first/last/middle/suffix fields (FR-002). Are these mutually exclusive, or should one parse into the other?

- [ ] CHK031 - Clarify: Should XConceptsEntry include all x-concept fields (wikidata, display_name, score) as per API spec? [Ambiguity, Spec §FR-005]
  - **Open Question**: FR-005 only lists "XConcepts: id" but OpenAlex API includes additional x-concept fields. Consider adding full field specification matching the API schema.

- [ ] CHK032 - Clarify: Are count/distinct_count integer type requirements explicit in the author model? [Ambiguity, Spec §FR-005]
  - **Open Question**: FR-005 doesn't enumerate `works_count`, `cited_by_count`, or any distinct_count fields that appear in test data. Consider adding complete field inventory from API docs.

---

## Dependencies & Assumptions (Are they documented and validated?)

- [ ] CHK033 - Is the OpenAlex Authors API documentation cited as authoritative contract? [Dependency, Spec §Assumptions]
  - **Validation**: Yes. Assumptions section explicitly states "The OpenAlex Authors documentation at https://developers.openalex.org/api-reference/authors.md is the baseline contract."

- [ ] CHK034 - Is Pydantic v2 with extra="allow" mode documented as the serialization library choice? [Dependency, Spec §QV-001]
  - **Validation**: Yes. QV-003 references "typing module for complex types", implying Python/Pydantic ecosystem. Assumptions confirm `pydantic.v1.Extra.allow mode` (consistent with Work model spec).

---

## Summary

### Passing Checks: 17
- CHK017, CHK026, CHK033, CHK034 and other validation passes
- Basic structure requirements are documented and testable

### Failing/Gap Checks: 15
- 5 completeness gaps (incomplete nested structure definitions)
- 8 clarity/consistency issues (field naming conventions, empty arrays, topic hierarchy)
- 2 traceability/documentation gaps (requirement ID scheme, API contract references in some sections)
- 3 edge case scenarios needing explicit documentation

### Recommendations:
1. Consolidate all reserved keyword aliases (id_, type_, two_year_mean_citedness) into FR-003 for clarity
2. Add explicit mention of empty array handling across all array fields
3. Clarify Affiliation vs Institution relationship to avoid implementation ambiguity
4. Document complete field inventory from API specification in FR-001 or FR-005

**Status**: Specification requires clarification on 15 items before implementation (mostly clarity gaps around field naming conventions and empty scenarios)
