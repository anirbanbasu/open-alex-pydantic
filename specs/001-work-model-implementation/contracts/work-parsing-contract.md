# Contract: Work Parsing Interface

## Scope

Defines the public parsing behavior contract for OpenAlex Work payloads in this package.

## Inputs

- A raw mapping payload representing one Work object from the OpenAlex API.
- Optional nested arrays/objects following OpenAlex Works schema.

## Outputs

- On success: an immutable `Work` model instance with strict typing and explicit alias behavior.
- On failure: a package-defined domain exception type for parsing/validation failure.

## Required Behaviors

1. Parsing supports documented Work payload fields represented by the model and nested model types.
2. Native snake_case names are preserved for non-conflicting fields.
3. Manual alias remaps are used only for conflict fields:
   - `id` <-> `id_`
   - `type` <-> `type_`
   - `license` <-> `license_`
4. Unknown/additive fields in payload do not fail parsing by themselves.
5. Invalid typed values fail under strict validation.
6. Public parsing APIs do not leak raw Pydantic `ValidationError` objects.

## Error Contract

- Domain exception class: implementation-defined package exception dedicated to Work parsing failures.
- Minimum exception payload:
  - message: human-readable summary
  - cause: retained original validation error object for debugging (non-public detail access)
- Stability requirement: callers should be able to catch one package-defined exception family for parsing failures.

## Serialization Expectations

- Serializing models with alias mode enabled returns native API field names.
- Reserved-name fields serialize as `id`, `type`, and `license` in API-shaped output.

## Test Assertions Required

- Valid sample payloads parse successfully.
- Reserved-name alias mapping is correct in both parse and dump directions.
- Extra unknown fields are accepted.
- Invalid payloads raise the domain exception at public parse boundary.
