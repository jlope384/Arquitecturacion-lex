from __future__ import annotations

from dataclasses import dataclass, field
from typing import Literal

from .grammar import Grammar, Production
from .lr0_automaton import LR0Automaton

Action = tuple[Literal["shift", "reduce", "accept", "error"], int | Production | None]


@dataclass
class SLRTable:
    action: dict[tuple[int, str], Action] = field(default_factory=dict)
    goto: dict[tuple[int, str], int] = field(default_factory=dict)
    conflicts: list[str] = field(default_factory=list)


def build_slr_table(grammar: Grammar, automaton: LR0Automaton) -> SLRTable:
    raise NotImplementedError
