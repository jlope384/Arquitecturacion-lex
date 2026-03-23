from __future__ import annotations

import argparse
from pathlib import Path

from yalexgen import YALexGenerator


def main() -> int:
    parser = argparse.ArgumentParser(description='YALex -> Python lexer generator')
    parser.add_argument('yal_file', help='Input .yal file')
    parser.add_argument('-o', '--output', required=True, help='Output generated Python lexer')
    parser.add_argument('--graph', help='Path to save expression tree PNG')
    args = parser.parse_args()

    gen = YALexGenerator()
    artifacts = gen.generate(args.yal_file, args.output, graph_path=args.graph)
    print(f'Generated lexer: {artifacts.python_path}')
    print(f'Expression tree: {artifacts.graph_path}')
    print(f'DFA states: {artifacts.dfa_state_count}')
    return 0


if __name__ == '__main__':
    raise SystemExit(main())
