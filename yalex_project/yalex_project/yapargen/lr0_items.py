from __future__ import annotations

from dataclasses import dataclass

from .grammar import Production


@dataclass(frozen=True)
class LR0Item:
    production: Production
    dot: int

    def next_symbol(self) -> str | None:
        if self.dot < len(self.production.body):
            return self.production.body[self.dot]
        return None

    def advance(self) -> LR0Item:
        return LR0Item(self.production, self.dot + 1)

    def is_complete(self) -> bool:
        return self.dot >= len(self.production.body)


ItemSet = frozenset[LR0Item]


def closure(items: ItemSet, productions_by_head: dict[str, list[Production]]) -> ItemSet:
    raise NotImplementedError


def goto(items: ItemSet, symbol: str, productions_by_head: dict[str, list[Production]]) -> ItemSet:
    raise NotImplementedError
