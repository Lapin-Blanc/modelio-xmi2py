# modelio-xmi2py

modelio-xmi2py is a professional-grade, test-driven toolchain that transforms UML models exported as XMI from **Modelio** into clean, typed **Python OOP code skeletons**.

> Scope: **Modelio-only**. The input format is the XMI produced by Modelio UML export.

## Goals

- Parse Modelio XMI exports reliably (with explicit contract)
- Build a stable internal representation (IR) of UML elements
- Apply configurable mapping rules (UML → Python)
- Generate readable Python code (type hints, minimal boilerplate)
- Ensure reproducibility via golden tests and fixtures

## Non-goals (for now)

- Supporting XMI produced by other UML tools
- Generating business logic implementations
- Supporting all UML diagram types (initial focus on class models)

## Supported (initial milestones)

- Classes
- Attributes
- Operations (method signatures)
- Inheritance (later milestone)
- Associations & multiplicities (later milestone)

## Quickstart (dev)

```bash
python -m venv .venv
source .venv/bin/activate
pip install -U pip
pip install -e ".[dev]"
pytest
ruff check .
ruff format .
