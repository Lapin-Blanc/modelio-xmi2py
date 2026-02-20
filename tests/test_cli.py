from __future__ import annotations

from pathlib import Path

from modelio_xmi2py.cli import main


def test_cli_main_smoke(tmp_path: Path) -> None:
    input_xmi = Path("tests/fixtures/modelio/simple.xmi")
    output_file = tmp_path / "out" / "model_gen.py"

    exit_code = main(["--input", str(input_xmi), "--output", str(output_file)])

    assert exit_code == 0
    assert output_file.exists()
