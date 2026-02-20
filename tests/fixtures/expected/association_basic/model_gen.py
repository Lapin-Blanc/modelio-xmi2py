from __future__ import annotations

from typing import Any


class A:
    def __init__(self, toA: B):
        self.toA = toA


class B:
    def __init__(self, toB: list[A]):
        self.toB = toB
