from __future__ import annotations

from pathlib import Path

from modelio_xmi2py.parser.modelio_xmi import parse_modelio_xmi

HERE = Path(__file__).parent

def test_real_modelio_export_smoke() -> None:
    xmi_path = HERE / "fixtures" / "modelio" / "real" / "library.xmi"
    classes = parse_modelio_xmi(xmi_path)

    assert len(classes) >= 1
    assert any(c.name == "Book" for c in classes)
