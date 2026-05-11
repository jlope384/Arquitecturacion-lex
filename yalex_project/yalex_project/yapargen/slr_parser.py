from __future__ import annotations

from .slr_table import SLRTable


class SLRParser:
    """Drive a parse using a pre-built SLR table."""

    def __init__(self, table: SLRTable) -> None:
        self.table = table

    def parse(self, tokens: list[str]) -> bool:
        raise NotImplementedError
