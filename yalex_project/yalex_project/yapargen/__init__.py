from __future__ import annotations

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from .yapar_parser import YAParParser

__all__ = ["YAParParser"]


def __getattr__(name: str):
    if name == "YAParParser":
        from .yapar_parser import YAParParser

        return YAParParser
    raise AttributeError(f"module {__name__!r} has no attribute {name!r}")
