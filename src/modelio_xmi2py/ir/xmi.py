from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path
from typing import Iterator
import xml.etree.ElementTree as ET

XMI_NAMESPACES = {
    "http://www.omg.org/XMI",
    "http://schema.omg.org/spec/XMI/2.0",
    "http://schema.omg.org/spec/XMI/2.1",
    "http://www.omg.org/spec/XMI/20131001",
}


@dataclass(slots=True)
class XmiNode:
    id: str | None
    xmi_type: str | None
    tag: str
    attrs: dict[str, str]
    children: list["XmiNode"]

    def attr(self, name: str, default: str | None = None) -> str | None:
        return self.attrs.get(name, default)

    def children_by_tag(self, tag: str) -> list["XmiNode"]:
        return [child for child in self.children if child.tag == tag]

    def iter(self) -> Iterator["XmiNode"]:
        yield self
        for child in self.children:
            yield from child.iter()


@dataclass(slots=True)
class XmiDocument:
    root: XmiNode
    by_id: dict[str, XmiNode]


def load_xmi_document(path: Path) -> XmiDocument:
    tree = ET.parse(Path(path))
    root_element = tree.getroot()
    by_id: dict[str, XmiNode] = {}
    root_node = _build_node(root_element, by_id)
    return XmiDocument(root=root_node, by_id=by_id)


def _build_node(element: ET.Element, by_id: dict[str, XmiNode]) -> XmiNode:
    attrs: dict[str, str] = {}
    xmi_id: str | None = None
    xmi_type: str | None = None

    for raw_name, value in element.attrib.items():
        namespace, local, key = _normalize_attr_name(raw_name)
        attrs[key] = value
        if namespace in XMI_NAMESPACES:
            if local == "id":
                xmi_id = value
            elif local == "type":
                xmi_type = value

    tag = _split_qname(element.tag)[1]
    node = XmiNode(id=xmi_id, xmi_type=xmi_type, tag=tag, attrs=attrs, children=[])

    if xmi_id is not None and xmi_id not in by_id:
        by_id[xmi_id] = node

    for child in list(element):
        node.children.append(_build_node(child, by_id))

    return node


def _split_qname(name: str) -> tuple[str | None, str]:
    if name.startswith("{"):
        namespace, local = name[1:].split("}", 1)
        return namespace, local
    return None, name


def _normalize_attr_name(name: str) -> tuple[str | None, str, str]:
    namespace, local = _split_qname(name)
    if namespace in XMI_NAMESPACES:
        return namespace, local, f"xmi:{local}"
    if namespace is None:
        return namespace, local, local
    return namespace, local, f"{{{namespace}}}{local}"
