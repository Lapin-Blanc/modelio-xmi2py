from __future__ import annotations

from pathlib import Path

from modelio_xmi2py.ir.uml import (
    AssociationEnd,
    Multiplicity,
    UmlAssociation,
    UmlAttribute,
    UmlClass,
    UmlOperation,
)
from modelio_xmi2py.ir.xmi import XmiDocument, XmiNode, load_xmi_document
from modelio_xmi2py.parser.resolve import ResolveContext


def parse_modelio_xmi(path: Path) -> list[UmlClass]:
    document = load_xmi_document(path)
    return _parse_modelio_xmi_document(document)


def _parse_modelio_xmi_document(document: XmiDocument) -> list[UmlClass]:
    ctx = ResolveContext(doc=document, by_id=document.by_id)

    # Pass 1: collect class nodes for the second pass.
    class_nodes: list[XmiNode] = []
    association_nodes: list[XmiNode] = []
    for node in document.root.iter():
        if node.tag != "packagedElement":
            continue
        if node.xmi_type == "uml:Class":
            class_nodes.append(node)
        elif node.xmi_type == "uml:Association":
            association_nodes.append(node)

    # Pass 2: build UML classes and resolve references.
    associations_by_class: dict[str, list[UmlAssociation]] = {}
    for assoc_node in association_nodes:
        association = _parse_association(ctx, assoc_node)
        if association is None:
            continue
        for end in association.ends:
            associations_by_class.setdefault(end.owner, []).append(association)

    classes: list[UmlClass] = []
    for node in class_nodes:
        class_name = node.attr("name")
        if not class_name:
            continue

        base_name: str | None = None
        generalization = _find_first_child(node, "generalization")
        if generalization is not None:
            general_id = generalization.attr("general")
            if general_id:
                resolved = ctx.resolve_id(general_id)
                base_name = resolved.attr("name") if resolved is not None else None

        attributes: list[UmlAttribute] = []
        for attr in _find_children(node, "ownedAttribute"):
            name = attr.attr("name")
            if name:
                python_type = "Any"
                type_id = attr.attr("type")
                if type_id:
                    resolved = ctx.resolve_id(type_id)
                    type_name = resolved.attr("name") if resolved is not None else None
                    python_type = _map_primitive_type(type_name)
                else:
                    type_elem = _find_first_child(attr, "type")
                    if type_elem is not None:
                        href = type_elem.attr("href")
                        if href and "#" in href:
                            type_name = href.split("#")[-1]
                            python_type = _map_primitive_type(type_name)

                attributes.append(UmlAttribute(name=name, python_type=python_type))

        operations: list[UmlOperation] = []
        for op in _find_children(node, "ownedOperation"):
            name = op.attr("name")
            if name:
                operations.append(UmlOperation(name=name))

        classes.append(
            UmlClass(
                name=class_name,
                attributes=sorted(attributes, key=lambda a: a.name),
                operations=sorted(operations, key=lambda o: o.name),
                base=base_name,
                associations=associations_by_class.get(class_name, []),
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


def _walk(node: XmiNode) -> list[XmiNode]:
    return list(node.iter())


def _find_children(node: XmiNode, tag: str) -> list[XmiNode]:
    return node.children_by_tag(tag)


def _find_first_child(node: XmiNode, tag: str) -> XmiNode | None:
    for child in node.children:
        if child.tag == tag:
            return child
    return None


def _parse_association(ctx: ResolveContext, node: XmiNode) -> UmlAssociation | None:
    ends = _collect_association_ends(ctx, node)
    if len(ends) != 2:
        return None

    end_specs: list[tuple[XmiNode, str, Multiplicity, str | None, bool | None]] = []
    for end_node in ends:
        type_id = end_node.attr("type")
        if not type_id:
            return None
        target_node = ctx.resolve_id(type_id)
        target_name = target_node.attr("name") if target_node is not None else None
        if not target_name:
            return None
        multiplicity = _parse_multiplicity(end_node)
        aggregation = end_node.attr("aggregation")
        navigable = _parse_bool(end_node.attr("isNavigable") or end_node.attr("navigable"))
        end_specs.append((end_node, target_name, multiplicity, aggregation, navigable))

    if len(end_specs) != 2:
        return None

    (end1_node, end1_target, end1_mult, end1_agg, end1_nav) = end_specs[0]
    (end2_node, end2_target, end2_mult, end2_agg, end2_nav) = end_specs[1]

    end1 = AssociationEnd(
        name=end1_node.attr("name"),
        owner=end1_target,
        target=end2_target,
        multiplicity=end1_mult,
        aggregation=end1_agg,
        navigable=end1_nav,
    )
    end2 = AssociationEnd(
        name=end2_node.attr("name"),
        owner=end2_target,
        target=end1_target,
        multiplicity=end2_mult,
        aggregation=end2_agg,
        navigable=end2_nav,
    )

    return UmlAssociation(name=node.attr("name"), ends=(end1, end2))


def _collect_association_ends(ctx: ResolveContext, node: XmiNode) -> list[XmiNode]:
    ends: list[XmiNode] = []

    member_end_attr = node.attr("memberEnd")
    if member_end_attr:
        for ref in member_end_attr.split():
            resolved = ctx.resolve_xmi_ref(ref)
            if resolved is not None:
                ends.append(resolved)

    ends.extend(node.children_by_tag("ownedEnd"))
    return ends


def _parse_multiplicity(node: XmiNode) -> Multiplicity:
    lower = _parse_multiplicity_value(node, "lowerValue", default=0)
    upper = _parse_multiplicity_value(node, "upperValue", default=1)
    return Multiplicity(lower=lower, upper=upper)


def _parse_multiplicity_value(node: XmiNode, tag: str, default: int | None) -> int | None:
    value_node = _find_first_child(node, tag)
    if value_node is None:
        return default
    value = value_node.attr("value")
    if value is None:
        return default
    if value == "*":
        return None
    try:
        return int(value)
    except ValueError:
        return default


def _parse_bool(value: str | None) -> bool | None:
    if value is None:
        return None
    if value.lower() in {"true", "1"}:
        return True
    if value.lower() in {"false", "0"}:
        return False
    return None
