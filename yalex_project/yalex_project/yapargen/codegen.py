from __future__ import annotations

from pathlib import Path
from typing import Union

from .slr_table import SLRTable
from .lalr_table import LALRTable

AnyTable = Union[SLRTable, LALRTable]


def generate_parser(table: AnyTable, output_path: str | Path) -> None:
    raise NotImplementedError
