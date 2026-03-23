from __future__ import annotations

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from .generator import YALexGenerator

__all__ = ["YALexGenerator"]


def __getattr__(name: str):
    if name == "YALexGenerator":
        from .generator import YALexGenerator

        return YALexGenerator
    raise AttributeError(f"module {__name__!r} has no attribute {name!r}")
