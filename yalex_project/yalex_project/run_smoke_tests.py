from __future__ import annotations

import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent


def run(cmd: list[str]) -> int:
    print('$', ' '.join(cmd))
    proc = subprocess.run(cmd, cwd=ROOT)
    print()
    return proc.returncode


def expect(cmd: list[str], expected: int) -> int:
    code = run(cmd)
    if code != expected:
        print(f'Expected exit code {expected}, got {code}')
        return 1
    return 0


def main() -> int:
    code = 0
    code |= expect([sys.executable, 'run_generator.py', 'examples/pico/pico.yal', '-o', 'build/pico_lexer.py', '--graph', 'build/pico_ast.png'], 0)
    code |= expect([sys.executable, 'build/pico_lexer.py', 'examples/pico/hello.pico', '--with-lexeme'], 0)
    code |= expect([sys.executable, 'build/pico_lexer.py', 'examples/pico/bad_string.pico'], 1)
    code |= expect([sys.executable, 'run_generator.py', 'examples/arnoldc/arnoldc.yal', '-o', 'build/arnold_lexer.py', '--graph', 'build/arnold_ast.png'], 0)
    code |= expect([sys.executable, 'build/arnold_lexer.py', 'examples/arnoldc/variables.arnoldc'], 0)
    code |= expect([sys.executable, 'build/arnold_lexer.py', 'examples/arnoldc/hash_comment.arnoldc'], 1)
    return code


if __name__ == '__main__':
    raise SystemExit(main())
