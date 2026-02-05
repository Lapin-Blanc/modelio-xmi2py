from __future__ import annotations

from pathlib import Path
from xml.etree import ElementTree

from modelio_xmi2py.ir.uml import UmlAttribute, UmlClass, UmlOperation


def parse_modelio_xmi(path: Path) -> list[UmlClass]:
    tree = ElementTree.parse(path)
    root = tree.getroot()

    classes: list[UmlClass] = []

    for packaged in root.findall(".//packagedElement"):
        if packaged.get("{http://www.omg.org/spec/XMI/20131001}type") != "uml:Class":
            continue
        class_name = packaged.get("name")
        if not class_name:
            continue

        attributes: list[UmlAttribute] = []
        for attr in packaged.findall("./ownedAttribute"):
            name = attr.get("name")
            if name:
                attributes.append(UmlAttribute(name=name))

        operations: list[UmlOperation] = []
        for op in packaged.findall("./ownedOperation"):
            name = op.get("name")
            if name:
                operations.append(UmlOperation(name=name))

        classes.append(
            UmlClass(
                name=class_name,
                attributes=sorted(attributes, key=lambda a: a.name),
                operations=sorted(operations, key=lambda o: o.name),
            )
        )

    return sorted(classes, key=lambda c: c.name)
