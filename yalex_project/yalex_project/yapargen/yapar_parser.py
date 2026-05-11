from __future__ import annotations

from pathlib import Path

from .grammar import Grammar


class YAParParser:
    """Parse a .yalp grammar file and return a Grammar object."""

    def parse_file(self, path: str | Path) -> Grammar:
        raise NotImplementedError

    def parse_string(self, src: str) -> Grammar:
        raise NotImplementedError
