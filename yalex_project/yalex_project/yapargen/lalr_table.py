from __future__ import annotations

from dataclasses import dataclass, field
from typing import Literal

from .grammar import Grammar, Production
from .lalr_automaton import LALRAutomaton

Action = tuple[Literal["shift", "reduce", "accept", "error"], int | Production | None]


@dataclass
class LALRTable:
    action: dict[tuple[int, str], Action] = field(default_factory=dict)
    goto: dict[tuple[int, str], int] = field(default_factory=dict)
    conflicts: list[str] = field(default_factory=list)


def build_lalr_table(grammar: Grammar, automaton: LALRAutomaton) -> LALRTable:
    raise NotImplementedError
