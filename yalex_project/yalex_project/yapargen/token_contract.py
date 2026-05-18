from __future__ import annotations

from dataclasses import dataclass, field


@dataclass
class Token:
    """A single token produced at runtime by the YALex-generated lexer.

    Attributes:
        type:    Token category name (e.g. ``"ID"``, ``"NUMBER"``).
                 Must match one of the names declared in the .yalex file.
        lexeme:  The exact source text that was matched.
        line:    1-based line number in the source file.
        column:  1-based column offset of the first character of the lexeme.
    """

    type: str
    lexeme: str
    line: int
    column: int


@dataclass
class YAParSpec:
    """Parsed representation of a .yapar specification file.

    This dataclass captures the three pieces of a .yapar file that matter
    for cross-module validation:

    Attributes:
        tokens:          Terminal names declared with ``%token`` directives
                         in the .yapar file (order preserved).
        ignore:          Terminal names declared with ``%ignore`` or listed
                         in whitespace-skip rules; the parser will silently
                         discard tokens of these types.
        raw_productions: The full unparsed production-rules section of the
                         .yapar source, kept verbatim for downstream use by
                         :mod:`yapargen.yapar_parser`.
    """

    tokens: list[str] = field(default_factory=list)
    ignore: list[str] = field(default_factory=list)
    raw_productions: str = ""


def validate_token_contract(
    yalex_tokens: list[str],
    yapar_spec: YAParSpec,
) -> list[str]:
    """Compare the token sets from YALex and YAPar and return mismatches.

    The YALex lexer owns the canonical set of token *type* names it can emit;
    the YAPar grammar references those names as terminals.  A mismatch means
    either the grammar references a token the lexer will never produce, or the
    lexer produces a token the grammar never consumes — both are worth flagging
    before the combined pipeline runs.

    Tokens listed in ``yapar_spec.ignore`` are intentionally omitted from the
    grammar productions, so they are excluded from the "only-in-YALex" check
    to avoid false positives.

    Args:
        yalex_tokens: List of token type names that the YALex-generated lexer
                      can emit (i.e. every ``return TOKEN_NAME`` found in the
                      .yalex rules, *excluding* ``lexbuf`` skips).
        yapar_spec:   Parsed .yapar specification containing the declared
                      ``%token`` list and the ``%ignore`` list.

    Returns:
        A list of human-readable warning strings, empty when the two token
        sets are perfectly consistent.  Each warning starts with either
        ``"[yapar-only]"`` (token declared in .yapar but never emitted by the
        lexer) or ``"[yalex-only]"`` (token emitted by the lexer but not
        declared in .yapar and not marked as ignored).
    """
    lex_set = set(yalex_tokens)
    par_set = set(yapar_spec.tokens)
    ignored = set(yapar_spec.ignore)

    warnings: list[str] = []

    for token in sorted(par_set - lex_set):
        warnings.append(
            f"[yapar-only] '{token}' is declared in the .yapar grammar "
            f"but is never emitted by the YALex lexer."
        )

    # Tokens the lexer emits that are neither consumed by the grammar nor
    # explicitly ignored are suspicious — the parser will choke on them.
    unconsumed = lex_set - par_set - ignored
    for token in sorted(unconsumed):
        warnings.append(
            f"[yalex-only] '{token}' is emitted by the YALex lexer "
            f"but is not declared in the .yapar grammar (and not ignored)."
        )

    return warnings
