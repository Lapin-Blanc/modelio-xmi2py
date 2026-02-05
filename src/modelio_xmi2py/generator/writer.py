from __future__ import annotations

from pathlib import Path
from typing import Any, Iterable

from modelio_xmi2py.ir.uml import UmlAttribute, UmlClass


def render_single_file(classes: Iterable[UmlClass]) -> str:
    classes_sorted = _topo_sort_classes(classes)

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

        lines.extend(_render_class(cls, classes_sorted))

    # Ensure trailing newline in file
    return "\n".join(lines) + "\n"


def write_single_file(classes: Iterable[UmlClass], output_file: Path) -> None:
    output_file.write_text(render_single_file(classes), encoding="utf-8")


def _render_class(cls: UmlClass, all_classes: Iterable[UmlClass]) -> list[str]:
    class_lines: list[str] = []
    if cls.base:
        class_lines.append(f"class {cls.name}({cls.base}):")
    else:
        class_lines.append(f"class {cls.name}:")

    attrs_sorted = _collect_all_attributes(cls, all_classes)
    ops_sorted = sorted(cls.operations, key=lambda o: o.name)

    if attrs_sorted:
        args = ", ".join([f"{a.name}: {a.python_type}" for a in attrs_sorted])
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


def _collect_all_attributes(cls: UmlClass, all_classes: Iterable[UmlClass]) -> list[UmlAttribute]:
    class_map = {c.name: c for c in all_classes}
    collected: list[UmlAttribute] = []
    seen: set[str] = set()

    current = cls
    lineage: list[UmlClass] = []
    while current.base and current.base in class_map:
        parent = class_map[current.base]
        lineage.append(parent)
        current = parent

    for ancestor in reversed(lineage):
        for attr in ancestor.attributes:
            if attr.name not in seen:
                collected.append(attr)
                seen.add(attr.name)

    for attr in sorted(cls.attributes, key=lambda a: a.name):
        if attr.name not in seen:
            collected.append(attr)
            seen.add(attr.name)

    return collected


def _topo_sort_classes(classes: Iterable[UmlClass]) -> list[UmlClass]:
    class_map = {c.name: c for c in classes}
    in_degree: dict[str, int] = {name: 0 for name in class_map}
    children: dict[str, list[str]] = {name: [] for name in class_map}

    for cls in class_map.values():
        if cls.base and cls.base in class_map:
            in_degree[cls.name] += 1
            children[cls.base].append(cls.name)

    ready = sorted([name for name, deg in in_degree.items() if deg == 0])
    ordered: list[UmlClass] = []

    while ready:
        name = ready.pop(0)
        ordered.append(class_map[name])
        for child in sorted(children[name]):
            in_degree[child] -= 1
            if in_degree[child] == 0:
                ready.append(child)
                ready.sort()

    if len(ordered) != len(class_map):
        return sorted(class_map.values(), key=lambda c: c.name)

    return ordered
