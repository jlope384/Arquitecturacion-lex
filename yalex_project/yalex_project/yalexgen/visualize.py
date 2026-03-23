from __future__ import annotations

import os
import tempfile
from dataclasses import dataclass
from pathlib import Path
from typing import Dict, List, Tuple

os.environ.setdefault("MPLCONFIGDIR", str(Path(tempfile.gettempdir()) / "yalexgen-mpl"))

import matplotlib

matplotlib.use("Agg")

import matplotlib.pyplot as plt

from .regex_ast import Charset, Concat, EOFMarker, Epsilon, Literal, OptionalNode, Plus, RegexNode, Star, Tagged, UnionNode


class ASTGrapher:
    def __init__(self):
        self.nodes: Dict[int, Tuple[str, List[int]]] = {}
        self._next = 0

    def build(self, root: RegexNode) -> int:
        nid = self._next
        self._next += 1
        label = self._label(root)
        children: List[int] = []
        if isinstance(root, (Concat, UnionNode)):
            children = [self.build(root.left), self.build(root.right)]
        elif isinstance(root, (Star, Plus, OptionalNode)):
            children = [self.build(root.child)]
        elif isinstance(root, Tagged):
            children = [self.build(root.child)]
        self.nodes[nid] = (label, children)
        return nid

    def _label(self, node: RegexNode) -> str:
        if isinstance(node, Literal):
            return repr(node.char)
        if isinstance(node, Charset):
            if node.label:
                return node.label
            preview = ''.join(sorted(node.chars)[:8])
            return f'[{preview}]'
        if isinstance(node, Epsilon):
            return 'ε'
        if isinstance(node, EOFMarker):
            return 'eof'
        if isinstance(node, Concat):
            return '·'
        if isinstance(node, UnionNode):
            return '|'
        if isinstance(node, Star):
            return '*'
        if isinstance(node, Plus):
            return '+'
        if isinstance(node, OptionalNode):
            return '?'
        if isinstance(node, Tagged):
            return node.tag
        return type(node).__name__

    def save_png(self, root: RegexNode, path: str, title: str = 'Expression Tree') -> None:
        self.nodes.clear()
        self._next = 0
        root_id = self.build(root)
        pos = self._tree_layout(root_id)
        depth = self._max_depth(root_id)
        width = min(28.0, max(10.0, len(self.nodes) * 0.18))
        height = min(18.0, max(6.0, depth * 1.1))
        plt.figure(figsize=(width, height))
        ax = plt.gca()
        node_size = max(220, 1200 - len(self.nodes) * 3)
        font_size = max(6, 11 - len(self.nodes) // 100)
        for nid, (label, children) in self.nodes.items():
            x, y = pos[nid]
            for child in children:
                cx, cy = pos[child]
                ax.plot([x, cx], [y, cy], color='gray', linewidth=1.5)
        for nid, (label, _) in self.nodes.items():
            x, y = pos[nid]
            ax.scatter([x], [y], s=node_size, color='#dff0d8', edgecolors='#2e7d32', linewidths=1.5, zorder=3)
            ax.text(x, y, label, ha='center', va='center', fontsize=font_size, zorder=4)
        ax.set_title(title)
        ax.axis('off')
        plt.tight_layout()
        plt.savefig(path, dpi=180, bbox_inches='tight')
        plt.close()

    def _max_depth(self, root_id: int) -> int:
        def visit(nid: int, depth: int) -> int:
            _, children = self.nodes[nid]
            if not children:
                return depth
            return max(visit(child, depth + 1) for child in children)

        return visit(root_id, 1)

    def _tree_layout(self, root_id: int):
        pos: Dict[int, Tuple[float, float]] = {}
        widths: Dict[int, int] = {}

        def measure(nid: int) -> int:
            label, children = self.nodes[nid]
            if not children:
                widths[nid] = 1
                return 1
            w = sum(measure(c) for c in children)
            widths[nid] = max(1, w)
            return widths[nid]

        def assign(nid: int, x0: float, depth: int):
            label, children = self.nodes[nid]
            width = widths[nid]
            center = x0 + width / 2.0
            pos[nid] = (center, -depth)
            child_x = x0
            for child in children:
                assign(child, child_x, depth + 1)
                child_x += widths[child]

        measure(root_id)
        assign(root_id, 0.0, 0)
        return pos
