from __future__ import annotations

from dataclasses import dataclass

from .grammar import Production


@dataclass(frozen=True)
class LR1Item:
    production: Production
    dot: int
    lookahead: str

    def next_symbol(self) -> str | None:
        if self.dot < len(self.production.body):
            return self.production.body[self.dot]
        return None

    def advance(self) -> LR1Item:
        return LR1Item(self.production, self.dot + 1, self.lookahead)

    def is_complete(self) -> bool:
        return self.dot >= len(self.production.body)


LR1ItemSet = frozenset[LR1Item]


def closure1(items: LR1ItemSet, productions_by_head: dict[str, list[Production]], first: dict[str, set[str]]) -> LR1ItemSet:
    raise NotImplementedError


def goto1(items: LR1ItemSet, symbol: str, productions_by_head: dict[str, list[Production]], first: dict[str, set[str]]) -> LR1ItemSet:
    raise NotImplementedError
