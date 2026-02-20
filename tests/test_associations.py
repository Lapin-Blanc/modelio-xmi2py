from __future__ import annotations

from pathlib import Path

from modelio_xmi2py.parser.modelio_xmi import parse_modelio_xmi

HERE = Path(__file__).parent


def test_parse_association_basic() -> None:
    xmi_path = HERE / "fixtures" / "xmi" / "association_basic.xmi"
    classes = parse_modelio_xmi(xmi_path)
    class_map = {cls.name: cls for cls in classes}

    assert "A" in class_map
    assert "B" in class_map

    a_associations = class_map["A"].associations
    b_associations = class_map["B"].associations

    assert len(a_associations) == 1
    assert len(b_associations) == 1
    assert a_associations[0] is b_associations[0]

    association = a_associations[0]
    assert association.name == "AtoB"
    end_a, end_b = association.ends

    assert {end_a.owner, end_b.owner} == {"A", "B"}
    assert {end_a.target, end_b.target} == {"A", "B"}

    for end in association.ends:
        if end.owner == "A":
            assert end.target == "B"
            assert end.multiplicity.lower == 1
            assert end.multiplicity.upper == 1
        else:
            assert end.target == "A"
            assert end.multiplicity.lower == 0
            assert end.multiplicity.upper is None
