from __future__ import annotations

from typing import Any


class Person:
    def __init__(self, name: Any):
        self.name = name


class Author(Person):
    def __init__(self, name: Any, pen_name: Any):
        self.name = name
        self.pen_name = pen_name
