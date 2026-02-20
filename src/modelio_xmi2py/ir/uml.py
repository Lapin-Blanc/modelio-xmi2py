from __future__ import annotations

from dataclasses import dataclass, field
from typing import List


@dataclass(frozen=True)
class UmlAttribute:
    name: str
    python_type: str = "Any"


@dataclass(frozen=True)
class UmlOperation:
    name: str


@dataclass(frozen=True)
class Multiplicity:
    lower: int | None
    upper: int | None


@dataclass(frozen=True)
class AssociationEnd:
    name: str | None
    owner: str
    target: str
    multiplicity: Multiplicity
    aggregation: str | None = None
    navigable: bool | None = None


@dataclass(frozen=True)
class UmlAssociation:
    name: str | None
    ends: tuple[AssociationEnd, AssociationEnd]


@dataclass(frozen=True)
class UmlClass:
    name: str
    attributes: List[UmlAttribute] = field(default_factory=list)
    operations: List[UmlOperation] = field(default_factory=list)
    base: str | None = None
    associations: List[UmlAssociation] = field(default_factory=list)
