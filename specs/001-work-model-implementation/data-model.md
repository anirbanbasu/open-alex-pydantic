# Data Model: Work Model Implementation Alignment

## Aggregate: Work

Represents a single OpenAlex Work payload with nested metadata objects.

### Core identity and publication fields

- `id_` (alias: `id`): optional string
- `doi`: optional string
- `title`: optional string
- `display_name`: optional string
- `publication_year`: optional integer
- `publication_date`: optional string
- `type_` (alias: `type`): optional string
- `language`: optional string

### Counts and status flags

- `cited_by_count`: optional integer
- `locations_count`: optional integer
- `referenced_works_count`: optional integer
- `countries_distinct_count`: optional integer (planned addition)
- `institutions_distinct_count`: optional integer (planned addition)
- `has_fulltext`: optional boolean (planned addition)
- `is_retracted`: optional boolean
- `is_paratext`: optional boolean
- `is_xpac`: optional boolean (planned addition)

### Nested objects

- `ids`: `WorkIds`
- `biblio`: `WorkBiblio`
- `primary_location`: `Location`
- `locations`: list of `Location`
- `best_oa_location`: `Location`
- `open_access`: `OpenAccess`
- `authorships`: list of `Authorship`
- `primary_topic`: `WorkTopic`
- `topics`: list of `WorkTopic`
- `keywords`: list of `WorkKeyword`
- `funders`: list of `DehydratedFunder`
- `awards`: list of `WorkAward`
- `apc_list`: `ApcInfo`
- `apc_paid`: `ApcInfo`
- `citation_normalized_percentile`: `CitationNormalizedPercentile`
- `cited_by_percentile_year`: `CitedByPercentileYear`
- `counts_by_year`: list of `WorkCountByYear`
- `sustainable_development_goals`: list of `WorkSustainableDevelopmentGoal`
- `mesh`: list of `MeshTag`
- `has_content`: `HasContent`
- `content_urls`: object with optional typed URL fields (planned addition)

### Collections and references

- `indexed_in`: list of strings
- `referenced_works`: list of strings
- `related_works`: list of strings
- `abstract_inverted_index`: mapping `str -> list[int]`

### Legacy/deprecated compatibility

- `concepts`: list of `WorkConcept` (retained)

## Nested Entities

### WorkIds

- `openalex`: optional string
- `doi`: optional string
- `mag`: optional string (planned type change from int for strict compatibility)
- `pmid`: optional string
- `pmcid`: optional string

### Location

- `id_` (alias: `id`): optional string (planned addition)
- `is_oa`: optional boolean
- `landing_page_url`: optional string
- `pdf_url`: optional string
- `source`: `DehydratedSource`
- `license_` (alias: `license`): optional string
- `license_id`: optional string
- `version`: optional string
- `is_accepted`: optional boolean
- `is_published`: optional boolean

### DehydratedSource

Current typed subset remains valid; additive source payload fields are accepted via extra-field tolerance.

### Authorship and related submodels

Current structure is retained, with additive field tolerance handling optional extras such as `raw_orcid` without breakage.

## Validation Rules

- Strict validation is required for all typed fields (no silent coercion).
- Model instances are immutable (frozen) after creation.
- Unknown/additive fields are tolerated to support API evolution.
- Alias mapping is manual and explicit only for reserved/built-in conflict names.

## Relationship Summary

- `Work` is the root aggregate.
- One-to-one optional links: `ids`, `biblio`, `open_access`, `primary_location`, `best_oa_location`.
- One-to-many links: `locations`, `authorships`, `topics`, `keywords`, `funders`, `awards`, `counts_by_year`, `mesh`, `sustainable_development_goals`, `concepts`, reference arrays.

## Error Model

- Public parse entry points must raise package-defined domain exceptions when payload validation fails.
- Raw Pydantic validation errors are internal details and must not cross the public parsing boundary.
