from __future__ import annotations

from dataclasses import dataclass


@dataclass
class Conflict:
    state: int
    symbol: str
    existing: object
    incoming: object
    kind: str


def report_conflicts(conflicts: list[Conflict]) -> None:
    raise NotImplementedError


def format_conflict(conflict: Conflict) -> str:
    raise NotImplementedError
