from __future__ import annotations

from pathlib import Path

from modelio_xmi2py.ir.xmi import load_xmi_document
from modelio_xmi2py.parser.resolve import ResolveContext

HERE = Path(__file__).parent


def test_resolve_xmi_idref() -> None:
    xmi_path = HERE / "fixtures" / "xmi" / "resolve_idref.xmi"
    document = load_xmi_document(xmi_path)
    ctx = ResolveContext(doc=document, by_id=document.by_id)

    source = document.by_id["c2"]
    ref_value = source.attrs["xmi:idref"]
    resolved = ctx.resolve_xmi_ref(ref_value)

    assert resolved is not None
    assert resolved.id == "c1"


def test_resolve_href_fragment_only() -> None:
    xmi_path = HERE / "fixtures" / "xmi" / "resolve_href_fragment.xmi"
    document = load_xmi_document(xmi_path)
    ctx = ResolveContext(doc=document, by_id=document.by_id)

    ref_node = next(node for node in document.root.iter() if node.tag == "ref")
    resolved = ctx.resolve_xmi_ref(ref_node.attrs["href"])

    assert resolved is not None
    assert resolved.id == "c1"


def test_resolve_order_reversed_fragment() -> None:
    xmi_path = HERE / "fixtures" / "xmi" / "resolve_order_reversed.xmi"
    document = load_xmi_document(xmi_path)
    ctx = ResolveContext(doc=document, by_id=document.by_id)

    ref_node = next(node for node in document.root.iter() if node.tag == "ref")
    resolved = ctx.resolve_xmi_ref(ref_node.attrs["href"])

    assert resolved is not None
    assert resolved.id == "c2"


def test_resolve_tracks_unresolved_refs() -> None:
    xmi_path = HERE / "fixtures" / "xmi" / "resolve_missing_href.xmi"
    document = load_xmi_document(xmi_path)
    ctx = ResolveContext(doc=document, by_id=document.by_id)

    ref_node = next(node for node in document.root.iter() if node.tag == "ref")
    resolved = ctx.resolve_xmi_ref(ref_node.attrs["href"])

    assert resolved is None
    assert "#missing" in ctx.unresolved
