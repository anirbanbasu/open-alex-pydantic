<!--
Sync Impact Report
- Version change: 2.0.0 -> 2.0.0
- Modified principles:
	- None
- Added sections:
	- None
- Removed sections:
	- None
- Templates requiring updates:
	- ✅ .specify/templates/plan-template.md
	- ✅ .specify/templates/spec-template.md
	- ✅ .specify/templates/tasks-template.md
	- ✅ .specify/templates/commands/*.md (not present in this repository; no update required)
- Deferred TODOs:
	- None
-->

# OpenAlex Pydantic Constitution

## Core Principles

### I. Test-First and 100% Delta Coverage (NON-NEGOTIABLE)
Every change MUST follow strict TDD: write failing tests first, implement the
smallest code change to pass, then refactor safely. New and modified code MUST
maintain 100% test coverage for the affected scope. No implementation work is
complete until failing-then-passing tests prove behavior.
Rationale: This project is a data-contract library where regressions silently
corrupt downstream analysis if behavior is not fully specified by tests.

### II. Strict Typing and Validation Contracts
All production code MUST target Python 3.12+ and use explicit type hints for
public and internal APIs. All request/response models MUST use Pydantic v2 with
strict validation behavior enabled. Validation semantics MUST be intentional,
documented in tests, and stable across releases.
Rationale: Strong static and runtime contracts make API schema drift visible and
prevent implicit coercions that hide upstream data quality issues.

### III. Immutable Native-Schema Model Design
Models MUST be configured as immutable using frozen model configuration.
Model fields MUST map directly to the OpenAlex API native snake_case property
names. Global alias generators MUST NOT be used. Manual aliases MAY be used
only to resolve Python reserved keywords or built-in conflicts and MUST map to
trailing-underscore equivalents, including at minimum id -> id_, type -> type_,
and license -> license_.
Rationale: Native schema mapping minimizes translation complexity and keeps
payload semantics explicit while preserving idiomatic Python naming only where
language rules require exceptions.

### IV. Defensive Parsing and Domain Exception Boundaries
Models MUST tolerate unexpected payload fields without breaking parsing unless a
schema rule explicitly forbids them. Parsing and validation failures MUST be
mapped to project-defined domain exceptions; raw third-party validation errors
MUST NOT leak through public interfaces.
Rationale: Consumers need stable failure modes and actionable errors even as the
OpenAlex API evolves.

### V. Compatibility and Minimal Surface Area
Public models and exception contracts MUST evolve conservatively. Breaking
changes to field names, aliases, error types, or strictness semantics MUST be
explicitly documented and versioned. New abstractions SHOULD be introduced only
when tests and repeated use cases justify them.
Rationale: A small, stable API surface keeps parsing behavior reliable for
long-lived clients and notebooks.

## Technical Standards

- Runtime MUST be Python 3.12 or newer.
- Pydantic MUST be version 2.x, and model validation MUST be configured for
	strict behavior by default.
- Model configuration MUST enforce immutability via frozen settings.
- Models MUST use native snake_case API field names directly with no global
	alias generators.
- Manual aliases MUST be limited to keyword/built-in conflict remaps to
	trailing underscores (at minimum id_, type_, license_).
- Parsing entry points MUST normalize validation failures into custom domain
	exceptions exposed by this package.

## Development Workflow and Quality Gates

1. Tests are authored first and MUST fail before implementation begins.
2. Each pull request MUST prove 100% coverage for all new and modified code.
3. Each pull request MUST include tests for strict validation, immutability,
	native snake_case field mapping, reserved-name manual aliases, and domain
	exception mapping when affected.
4. Code review MUST reject changes that bypass domain exceptions or weaken type
	and validation guarantees.
5. Release notes MUST call out any contract-impacting changes.

## Governance
<!-- Example: Constitution supersedes all other practices; Amendments require documentation, approval, migration plan -->

This constitution is the authoritative engineering policy for this repository.
All plans, specs, tasks, and pull requests MUST pass constitution checks.
Amendments require a documented pull request that includes: rationale, impact,
version bump classification, and updates to affected templates or guidance.

Versioning policy:
- MAJOR: Removal or incompatible redefinition of a core principle or mandatory
	quality gate.
- MINOR: Addition of a principle/section or materially stricter governance.
- PATCH: Clarifications and non-semantic wording improvements.

Compliance review is required during planning, task generation, code review, and
release preparation.

**Version**: 2.0.0 | **Ratified**: 2026-06-28 | **Last Amended**: 2026-06-28
