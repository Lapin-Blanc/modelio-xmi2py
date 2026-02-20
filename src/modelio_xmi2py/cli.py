from __future__ import annotations

import argparse
import sys
from pathlib import Path
from typing import Sequence

from modelio_xmi2py.generator.writer import write_single_file
from modelio_xmi2py.parser.modelio_xmi import parse_modelio_xmi


def generate_single_file(input_xmi: Path, output_file: Path) -> None:
    classes = parse_modelio_xmi(input_xmi)
    output_file.parent.mkdir(parents=True, exist_ok=True)
    write_single_file(classes, output_file)


def main(argv: Sequence[str] | None = None) -> int:
    parser = argparse.ArgumentParser(
        prog="modelio-xmi2py",
        description="Generate a Python model file from a Modelio UML XMI export.",
    )
    parser.add_argument("--input", type=Path, required=True, help="Path to the input XMI file.")
    parser.add_argument("--output", type=Path, required=True, help="Path to the generated Python file.")
    args = parser.parse_args(list(argv) if argv is not None else None)

    try:
        generate_single_file(input_xmi=args.input, output_file=args.output)
    except Exception as exc:  # pragma: no cover - exercised via dedicated error test if added
        print(f"Error: {exc}", file=sys.stderr)
        return 1
    return 0
