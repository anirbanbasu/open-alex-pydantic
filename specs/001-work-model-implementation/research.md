# Research: Work Model Implementation Alignment

## Decision 1: Base model configuration must combine strict validation, immutability, and additive-field tolerance

- Decision: Update shared entity configuration so models are strict and frozen while allowing unknown fields (`extra='allow'`) for forward-compatible payload parsing.
- Rationale: Constitution requires strict validation and immutability, while also requiring graceful handling of unexpected payload fields. A centralized base configuration ensures nested Work submodels inherit consistent behavior.
- Alternatives considered:
  - Keep current default BaseModel behavior: rejected because it does not guarantee strict mode or immutability.
  - Forbid extra fields: rejected because it violates defensive parsing requirements for additive API changes.
  - Ignore extras globally: rejected because unknown fields should remain inspectable when needed.

## Decision 2: Preserve native snake_case names and use explicit aliases only for reserved/built-in conflicts

- Decision: Keep API-native names as field names and use explicit aliases only for conflict cases (`id`, `type`, `license` mapped to `id_`, `type_`, `license_`).
- Rationale: This is a direct constitution requirement and avoids hidden name-translation logic.
- Alternatives considered:
  - Use global alias generator: rejected due to explicit prohibition.
  - Rename many fields to Pythonic variants: rejected because it drifts from source schema and increases mapping complexity.

## Decision 3: Model schema must be reconciled against real Works payload shape from documentation and fixtures

- Decision: Expand/update Work and nested models to account for documented and observed payload structures used by current fixtures, including:
  - `Location.id`
  - top-level `content_urls` object (instead of only `content_url` string)
  - optional top-level counters/flags such as `has_fulltext`, `is_xpac`, and distinct-count fields
  - `ids.mag` represented as string in fixture data
- Rationale: Current sample payloads and Works documentation include these fields; missing or mismatched typing causes avoidable validation failures under strict mode.
- Alternatives considered:
  - Keep only minimal schema and rely on extras: rejected because key fields should be represented explicitly for typed access and testability.
  - Coerce mismatched input types (e.g., string to int): rejected because strict mode must avoid silent coercion.

## Decision 4: Public parsing must map failures to domain exceptions

- Decision: Add a project-defined Work parsing exception and a public parse entry point that catches validation errors and raises the domain exception.
- Rationale: Constitution requires stable package-level error contracts and no leakage of raw third-party validation errors at public boundaries.
- Alternatives considered:
  - Expose raw ValidationError directly: rejected by constitution.
  - Wrap errors ad hoc in tests only: rejected because contract must be implemented in package code.

## Decision 5: Test strategy must become behavior-focused and constitution-complete

- Decision: Extend tests beyond smoke parsing of fixture files to include strictness, immutability, alias behavior, unknown-field tolerance, and domain exception mapping.
- Rationale: Constitution requires strict TDD and 100% coverage for changed scope; simple parse smoke tests are insufficient to prove required behavior.
- Alternatives considered:
  - Keep only fixture parse tests: rejected due to coverage and contract gaps.
  - Add only unit tests for isolated helpers: rejected because end-to-end parsing behavior is the primary user contract.
