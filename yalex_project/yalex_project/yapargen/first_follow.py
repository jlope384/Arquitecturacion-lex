from __future__ import annotations

from .grammar import Grammar

EPSILON = ""


def compute_first(grammar: Grammar) -> dict[str, set[str]]:
    raise NotImplementedError


def compute_follow(grammar: Grammar, first: dict[str, set[str]]) -> dict[str, set[str]]:
    raise NotImplementedError
