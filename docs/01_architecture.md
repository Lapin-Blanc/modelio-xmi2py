# Architecture

The tool follows a layered pipeline.

## Pipeline

1. **Parser**
   - Reads Modelio XMI (XML)
   - Extracts UML elements according to the Modelio contract
   - Produces an internal representation (IR)

2. **IR (Intermediate Representation)**
   - Python dataclasses representing UML concepts
   - Stable and testable
   - No generator-specific logic

3. **Mapping**
   - Converts IR UML concepts into Python-oriented structures
   - Applies type mapping and multiplicity rules
   - Handles naming conventions and sanitization

4. **Generator**
   - Writes Python source files
   - Ensures formatting and deterministic ordering
   - Outputs either:
     - single file (early milestones)
     - package/module structure (later milestones)

5. **CLI**
   - Entry point
   - Reads config (later)
   - Orchestrates parse → map → generate

## Design principles

- Separation of concerns (no XML parsing in generator)
- Determinism (stable ordering, stable formatting)
- Explicit errors (clear exceptions for unsupported patterns)
- Testability (IR and mapping functions are unit-testable)
