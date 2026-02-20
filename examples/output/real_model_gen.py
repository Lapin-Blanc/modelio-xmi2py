from __future__ import annotations

from typing import Any


class Book:
    def __init__(self, pages: int, summary: str, title: str):
        self.pages = pages
        self.summary = summary
        self.title = title
