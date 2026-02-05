from __future__ import annotations

from typing import Any


class Book:
    def __init__(self, pages: int, published: bool, rating: float, title: str):
        self.pages = pages
        self.published = published
        self.rating = rating
        self.title = title
