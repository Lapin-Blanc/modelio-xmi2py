# Modelio XMI contract (input)

This document specifies the subset of XMI produced by **Modelio** that this tool supports.

## Assumptions

- The input is an XMI export generated from Modelio UML.
- UML elements are represented using UML 2.x style `packagedElement`, `ownedAttribute`, etc.
- Namespaces and ids must be resolved reliably.

## Elements to parse (initial)

### Classes
- `packagedElement` with `xmi:type="uml:Class"`
- required: `name`
- id: `xmi:id`

### Attributes
- `ownedAttribute`
- required: `name`
- optional: `type` (may be an idref to a primitive or another class)
- optional: multiplicity info (later milestone)

### Operations
- `ownedOperation`
- required: `name`
- parameters: `ownedParameter`
  - `direction="return"` for return type (if present)
  - otherwise method parameters

## Type resolution rules

- If `type` is an idref and the target has a name, use that name.
- If type cannot be resolved, default to `Any` and emit a warning.

## Ordering rules (determinism)

- Classes: sort by fully qualified name (package + class)
- Attributes and operations: sort by name (tie-breaker by XMI id)

## Known variations (to handle over time)

- Namespaces differ by Modelio version
- Primitive types might be embedded or referenced differently

## Test fixtures

All supported patterns must be represented in `tests/fixtures/modelio/`.
