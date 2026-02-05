# Testing strategy

We combine unit tests and golden tests.

## Unit tests

- Parser:
  - namespace handling
  - class extraction
  - attribute extraction
  - operation extraction
- Mapping:
  - type mapping
  - identifier sanitization

## Golden tests (deterministic generation)

- For each fixture XMI input:
  - run the pipeline
  - compare generated output against `tests/fixtures/expected/<case>/...`
- Golden outputs are considered canonical and must be updated intentionally.

## Fixtures

`tests/fixtures/modelio/` contains representative Modelio XMI exports:
- simple classes
- inheritance
- associations
- edge cases

## Rules

- Any bug fix requires a fixture reproducing the issue.
- Any change to generation must be accompanied by updated golden outputs.
