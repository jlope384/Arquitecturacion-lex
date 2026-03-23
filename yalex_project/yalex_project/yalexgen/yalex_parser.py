from __future__ import annotations

from dataclasses import dataclass
from typing import Dict, List, Optional


class YALexParseError(Exception):
    pass


@dataclass
class RuleEntry:
    regex_text: str
    action_text: str
    order: int


@dataclass
class YALexSpec:
    header: str
    trailer: str
    definitions: Dict[str, str]
    entrypoint: str
    entries: List[RuleEntry]
    raw_text: str


class YALexParser:
    def parse(self, text: str) -> YALexSpec:
        clean = self._strip_comments(text)
        i = 0
        n = len(clean)
        header = ''
        trailer = ''
        definitions: Dict[str, str] = {}

        i = self._skip_ws(clean, i)
        if i < n and clean[i] == '{':
            header, i = self._read_brace_block(clean, i)
        while True:
            i = self._skip_ws(clean, i)
            if clean.startswith('let', i) and self._is_word_boundary(clean, i - 1) and self._is_word_boundary(clean, i + 3):
                i += 3
                i = self._skip_ws(clean, i)
                name, i = self._read_identifier(clean, i)
                i = self._skip_ws(clean, i)
                if i >= n or clean[i] != '=':
                    raise YALexParseError(f"Expected '=' after let {name}")
                i += 1
                expr_start = i
                while i < n and clean[i] != '\n':
                    i += 1
                expr = clean[expr_start:i].strip()
                definitions[name] = expr
                continue
            break
        i = self._skip_ws(clean, i)
        if not clean.startswith('rule', i):
            raise YALexParseError('Expected rule entrypoint = ... block')
        i += 4
        i = self._skip_ws(clean, i)
        entrypoint, i = self._read_identifier(clean, i)
        i = self._skip_ws(clean, i)
        # Ignore optional [args]
        if i < n and clean[i] == '[':
            depth = 1
            i += 1
            while i < n and depth > 0:
                if clean[i] == '[':
                    depth += 1
                elif clean[i] == ']':
                    depth -= 1
                i += 1
        i = self._skip_ws(clean, i)
        if i >= n or clean[i] != '=':
            raise YALexParseError("Expected '=' after rule entrypoint")
        i += 1

        entries: List[RuleEntry] = []
        order = 0
        while True:
            i = self._skip_ws(clean, i)
            if i >= n:
                break
            if clean[i] == '{':
                trailer, i = self._read_brace_block(clean, i)
                i = self._skip_ws(clean, i)
                if i != n:
                    rest = clean[i:].strip()
                    if rest:
                        raise YALexParseError(f'Unexpected content after trailer: {rest[:40]!r}')
                break
            if clean[i] == '|':
                i += 1
                i = self._skip_ws(clean, i)
            regex_text, i = self._read_regex_until_action(clean, i)
            i = self._skip_ws(clean, i)
            if i >= n or clean[i] != '{':
                raise YALexParseError(f'Missing action block for rule regex {regex_text!r}')
            action, i = self._read_brace_block(clean, i)
            entries.append(RuleEntry(regex_text=regex_text.strip(), action_text=action.strip(), order=order))
            order += 1
        if not entries:
            raise YALexParseError('No rule entries found')
        return YALexSpec(header=header.strip(), trailer=trailer.strip(), definitions=definitions, entrypoint=entrypoint, entries=entries, raw_text=text)

    def _strip_comments(self, text: str) -> str:
        out: List[str] = []
        i = 0
        n = len(text)
        in_squote = False
        in_dquote = False
        while i < n:
            c = text[i]
            if c == '\\':
                if i + 1 < n:
                    out.append(text[i])
                    out.append(text[i + 1])
                    i += 2
                else:
                    out.append(c)
                    i += 1
                continue
            if not in_squote and not in_dquote and text.startswith('(*', i):
                end = text.find('*)', i + 2)
                if end == -1:
                    raise YALexParseError('Unterminated comment (* ... *)')
                i = end + 2
                continue
            if c == "'" and not in_dquote:
                in_squote = not in_squote
            elif c == '"' and not in_squote:
                in_dquote = not in_dquote
            out.append(c)
            i += 1
        return ''.join(out)

    def _skip_ws(self, text: str, i: int) -> int:
        while i < len(text) and text[i].isspace():
            i += 1
        return i

    def _is_word_boundary(self, text: str, i: int) -> bool:
        if i < 0 or i >= len(text):
            return True
        return not (text[i].isalnum() or text[i] == '_')

    def _read_identifier(self, text: str, i: int):
        start = i
        if i >= len(text) or not (text[i].isalpha() or text[i] == '_'):
            raise YALexParseError(f'Expected identifier at position {i}')
        i += 1
        while i < len(text) and (text[i].isalnum() or text[i] == '_'):
            i += 1
        return text[start:i], i

    def _read_brace_block(self, text: str, i: int):
        assert text[i] == '{'
        depth = 1
        i += 1
        start = i
        in_squote = False
        in_dquote = False
        while i < len(text):
            c = text[i]
            if c == '\\':
                i += 2
                continue
            if c == "'" and not in_dquote:
                in_squote = not in_squote
            elif c == '"' and not in_squote:
                in_dquote = not in_dquote
            elif not in_squote and not in_dquote:
                if c == '{':
                    depth += 1
                elif c == '}':
                    depth -= 1
                    if depth == 0:
                        return text[start:i], i + 1
            i += 1
        raise YALexParseError('Unterminated brace block')

    def _read_regex_until_action(self, text: str, i: int):
        start = i
        depth_paren = 0
        depth_bracket = 0
        in_squote = False
        in_dquote = False
        while i < len(text):
            c = text[i]
            if c == '\\':
                i += 2
                continue
            if c == "'" and not in_dquote and depth_bracket == 0:
                in_squote = not in_squote
                i += 1
                continue
            if c == '"' and not in_squote and depth_bracket == 0:
                in_dquote = not in_dquote
                i += 1
                continue
            if not in_squote and not in_dquote:
                if c == '[':
                    depth_bracket += 1
                elif c == ']':
                    depth_bracket -= 1
                elif depth_bracket == 0:
                    if c == '(':
                        depth_paren += 1
                    elif c == ')':
                        depth_paren -= 1
                    elif c == '{' and depth_paren == 0:
                        return text[start:i].rstrip(), i
            i += 1
        raise YALexParseError('Could not find action block for regex')
