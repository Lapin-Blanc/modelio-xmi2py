from __future__ import annotations

from pathlib import Path

from modelio_xmi2py.generator.writer import write_single_file
from modelio_xmi2py.parser.modelio_xmi import parse_modelio_xmi


def generate_single_file(input_xmi: Path, output_file: Path) -> None:
    classes = parse_modelio_xmi(input_xmi)
    write_single_file(classes, output_file)


def main() -> None:
    raise SystemExit("CLI entrypoint not implemented for M1.")
