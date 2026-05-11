from __future__ import annotations

from typing import Union

from .slr_table import SLRTable
from .lalr_table import LALRTable

AnyTable = Union[SLRTable, LALRTable]


def run_parse(table: AnyTable, tokens: list[str]) -> bool:
    raise NotImplementedError
