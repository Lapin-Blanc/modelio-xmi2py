# Codex playbook (working rules)

This repository is designed to be developed with the help of Codex.  
Codex contributions must comply with the following rules.

## Non-negotiables

- Do not broaden scope beyond **Modelio XMI**.
- Keep parser / IR / mapping / generator responsibilities separated.
- Do not change golden outputs without updating fixtures and documenting why.
- Prefer small, reviewable commits.

## Development workflow

1. Update or create fixtures first (`tests/fixtures/modelio/`)
2. Write or update tests (unit or golden)
3. Implement the smallest change to make tests pass
4. Run:
   - `pytest`
   - `ruff check .`
   - `ruff format .`
   - `mypy src`

## Coding conventions

- Python >= 3.11
- Typed code (mypy strict settings)
- dataclasses for IR objects
- deterministic ordering everywhere (sort keys, stable output)

## Implementation notes

- XML parsing must handle namespaces robustly
- Type resolution must degrade gracefully:
  - unresolved types → `Any` + warning
- Prefer explicit exceptions with meaningful messages:
  - `UnsupportedModelioXMIError`
  - `XMIParseError`
  - `GenerationError`

## Milestones (suggested)

M1: parse classes/attributes/operations + single-file generator + golden tests  
M2: type mapping primitives + mypy-clean  
M3: inheritance  
M4: associations & multiplicity  
M5: packages → modules + config YAML
