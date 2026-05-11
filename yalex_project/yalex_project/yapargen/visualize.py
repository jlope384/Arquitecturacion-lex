from __future__ import annotations

from pathlib import Path
from typing import Union

from .lr0_automaton import LR0Automaton
from .lalr_automaton import LALRAutomaton

AnyAutomaton = Union[LR0Automaton, LALRAutomaton]


def render_automaton(automaton: AnyAutomaton, output_path: str | Path) -> None:
    raise NotImplementedError


def render_parse_tree(tree: object, output_path: str | Path) -> None:
    raise NotImplementedError
