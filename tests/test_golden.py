from __future__ import annotations

from pathlib import Path

from modelio_xmi2py.cli import generate_single_file


def test_golden_simple(tmp_path: Path) -> None:
    fixture = Path("tests/fixtures/modelio/simple.xmi")
    out_file = tmp_path / "model_gen.py"

    generate_single_file(input_xmi=fixture, output_file=out_file)

    expected = Path("tests/fixtures/expected/simple/model_gen.py").read_text(encoding="utf-8").strip()
    actual = out_file.read_text(encoding="utf-8").strip()

    assert actual == expected
