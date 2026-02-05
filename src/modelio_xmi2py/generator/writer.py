from __future__ import annotations

from pathlib import Path
from typing import Any, Iterable

from modelio_xmi2py.ir.uml import UmlClass


def render_single_file(classes: Iterable[UmlClass]) -> str:
    # Deterministic ordering
    classes_sorted = sorted(classes, key=lambda c: c.name)

    lines: list[str] = []
    lines.append("from __future__ import annotations")
    lines.append("")
    lines.append("from typing import Any")
    lines.append("")
    lines.append("")

    first_class = True
    for cls in classes_sorted:
        if not first_class:
            lines.append("")
            lines.append("")
        first_class = False

        lines.extend(_render_class(cls))

    # Ensure trailing newline in file
    return "\n".join(lines) + "\n"


def write_single_file(classes: Iterable[UmlClass], output_file: Path) -> None:
    output_file.write_text(render_single_file(classes), encoding="utf-8")


def _render_class(cls: UmlClass) -> list[str]:
    class_lines: list[str] = []
    class_lines.append(f"class {cls.name}:")

    attrs_sorted = sorted(cls.attributes, key=lambda a: a.name)
    ops_sorted = sorted(cls.operations, key=lambda o: o.name)

    if attrs_sorted:
        args = ", ".join([f"{a.name}: Any" for a in attrs_sorted])
        class_lines.append(f"    def __init__(self, {args}):")
        for a in attrs_sorted:
            class_lines.append(f"        self.{a.name} = {a.name}")
    else:
        class_lines.append("    def __init__(self):")
        class_lines.append("        pass")

    # Operations (M1: no params; return None)
    for op in ops_sorted:
        class_lines.append("")
        class_lines.append(f"    def {op.name}(self) -> None:")
        class_lines.append("        pass")

    return class_lines
