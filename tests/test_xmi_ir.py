from __future__ import annotations

from pathlib import Path

from modelio_xmi2py.ir.xmi import XmiNode, load_xmi_document

HERE = Path(__file__).parent


def _walk(node: XmiNode) -> list[XmiNode]:
    nodes = [node]
    for child in node.children:
        nodes.extend(_walk(child))
    return nodes


def test_xmi_ir_real_modelio_export() -> None:
    xmi_path = HERE / "fixtures" / "modelio" / "real" / "library.xmi"
    document = load_xmi_document(xmi_path)

    nodes = _walk(document.root)
    assert any(node.xmi_type == "uml:Class" for node in nodes)

    assert len(document.by_id) >= 1
    sample_id, sample_node = next(iter(document.by_id.items()))
    assert sample_node.id == sample_id
