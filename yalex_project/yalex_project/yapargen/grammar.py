from __future__ import annotations

from dataclasses import dataclass, field


@dataclass(frozen=True)
class Production:
    head: str
    body: tuple[str, ...]

    def __len__(self) -> int:
        return len(self.body)


@dataclass
class Grammar:
    terminals: set[str] = field(default_factory=set)
    non_terminals: set[str] = field(default_factory=set)
    productions: list[Production] = field(default_factory=list)
    start: str = ""

    def add_production(self, head: str, body: tuple[str, ...]) -> Production:
        p = Production(head, body)
        self.productions.append(p)
        self.non_terminals.add(head)
        return p

    def augment(self) -> Grammar:
        raise NotImplementedError
