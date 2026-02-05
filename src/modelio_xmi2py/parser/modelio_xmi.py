from __future__ import annotations

from pathlib import Path
from xml.etree import ElementTree

from modelio_xmi2py.ir.uml import UmlAttribute, UmlClass, UmlOperation


def parse_modelio_xmi(path: Path) -> list[UmlClass]:
    tree = ElementTree.parse(path)
    root = tree.getroot()

    id_to_name: dict[str, str] = {}
    for packaged in root.findall(".//packagedElement"):
        element_id = _get_attr_by_localname(packaged, "id")
        name = packaged.get("name")
        if element_id and name:
            id_to_name[element_id] = name

    classes: list[UmlClass] = []

    for packaged in root.findall(".//packagedElement"):
        if _get_attr_by_localname(packaged, "type") != "uml:Class":
            continue
        class_name = packaged.get("name")
        if not class_name:
            continue

        base_name: str | None = None
        generalization = packaged.find("./generalization")
        if generalization is not None:
            general_id = generalization.get("general")
            base_name = id_to_name.get(general_id or "")

        attributes: list[UmlAttribute] = []
        for attr in packaged.findall("./ownedAttribute"):
            name = attr.get("name")
            if name:
                python_type = "Any"
                type_id = attr.get("type")
                if type_id:
                    type_name = id_to_name.get(type_id or "")
                    python_type = _map_primitive_type(type_name)
                else:
                    type_elem = _find_child_by_localname(attr, "type")
                    if type_elem is not None:
                        href = _get_attr_by_localname(type_elem, "href")
                        if href and "#" in href:
                            type_name = href.split("#")[-1]
                            python_type = _map_primitive_type(type_name)

                attributes.append(UmlAttribute(name=name, python_type=python_type))

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
                base=base_name,
            )
        )

    return sorted(classes, key=lambda c: c.name)


def _map_primitive_type(type_name: str | None) -> str:
    if type_name == "String":
        return "str"
    if type_name == "Integer":
        return "int"
    if type_name == "Boolean":
        return "bool"
    if type_name == "Real":
        return "float"
    return "Any"


def _get_attr_by_localname(elem: ElementTree.Element, localname: str) -> str | None:
    for key, value in elem.attrib.items():
        if key.split("}")[-1] == localname:
            return value
    return None


def _find_child_by_localname(elem: ElementTree.Element, localname: str) -> ElementTree.Element | None:
    for child in elem:
        if child.tag.split("}")[-1] == localname:
            return child
    return None
