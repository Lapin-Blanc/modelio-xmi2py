# Mapping specification (UML → Python)

## Naming

- Class names: preserved, but sanitized to valid Python identifiers if needed.
- Attribute names: converted to snake_case if configured (default: preserve).
- Method names: preserve, sanitize if needed.

## Type mapping (initial)

| UML | Python |
|-----|--------|
| String | str |
| Integer | int |
| Boolean | bool |
| Real | float |
| Date | datetime.date |
| DateTime | datetime.datetime |

If a type is unknown or unresolved:
- use `Any`
- emit a warning

## Attributes

UML attribute → instance attribute.

Default behavior:
- generate `__init__` with parameters for attributes
- assign `self.attr = attr`

Option (later):
- generate `@dataclass`

## Operations

UML operation → method stub with `pass`.

- parameters become method parameters (best-effort typing)
- return parameter becomes return type (default: `None`)

## Multiplicity (later milestone)

- `0..1` → `Optional[T]`
- `1` → `T`
- `0..*` or `*` → `List[T]`
