# CLI specification

## Command

`modelio-xmi2py <input.xmi> -o <output_dir> [--config mapping.yml] [--single-file] [--verbose]`

## Arguments

- `input.xmi`: path to Modelio XMI export
- `-o / --output`: output directory
- `--config`: mapping configuration file (future milestone)
- `--single-file`: force generation into a single python file (early milestone)
- `--verbose`: enable debug logs

## Exit codes

- `0`: success
- `1`: parsing/generation error
- `2`: invalid CLI usage

## Output conventions

- Early milestone: `out/model_gen.py`
- Later: package structure based on UML packages
