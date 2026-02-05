from __future__ import annotations

from typing import Any


class Author:
    def __init__(self, name: Any):
        self.name = name


class Book:
    def __init__(self, pages: Any, title: Any):
        self.pages = pages
        self.title = title

    def summary(self) -> None:
        pass
