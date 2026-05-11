from __future__ import annotations

from dataclasses import dataclass, field

from .grammar import Grammar
from .lr1_items import LR1ItemSet


@dataclass
class LALRAutomaton:
    states: list[LR1ItemSet] = field(default_factory=list)
    transitions: dict[tuple[int, str], int] = field(default_factory=dict)
    start_state: int = 0


def build_lalr_automaton(grammar: Grammar) -> LALRAutomaton:
    raise NotImplementedError
