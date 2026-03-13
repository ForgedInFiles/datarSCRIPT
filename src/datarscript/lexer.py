"""Tokenizer for DatarScript source code."""

from __future__ import annotations

import re
from dataclasses import dataclass
from typing import Iterator

from .errors import DatarSyntaxError


@dataclass(frozen=True)
class Token:
    type: str  # Can be a string like "IDENT" or TokenType.EOF
    value: str
    lineno: int

    def __repr__(self) -> str:
        type_name = self.type if isinstance(self.type, str) else self.type.name
        return f"Token({type_name!r}, {self.value!r}, line={self.lineno})"


class TokenType:
    # Special
    EOF = "EOF"
    IDENT = "IDENT"  # variable/function names
    NUMBER = "NUMBER"
    STRING = "STRING"
    BOOLEAN = "BOOLEAN"  # true, false
    NULL = "NULL"  # null, none, nothing

    # Punctuation
    COLON = "COLON"
    COMMA = "COMMA"
    DOT = "DOT"
    LPAREN = "LPAREN"
    RPAREN = "RPAREN"
    LBRACK = "LBRACK"
    RBRACK = "RBRACK"
    LBRACE = "LBRACE"
    RBRACE = "RBRACE"

    @classmethod
    def get(cls, name: str) -> str:
        """Get token type string by name."""
        return getattr(cls, name, name)

    # For convenience, we don't create separate operator token; treat multi-word operators in parser.


class Lexer:
    """Converts source code string into a stream of Tokens."""

    TOKEN_SPEC = [
        ("WHITESPACE", r"[ \t]+"),
        ("NEWLINE", r"\n"),
        ("COMMENT", r"#(?!.*['\"]).*"),
        ("STRING", r'"(?:[^"\\]|\\.)*"'),
        ("NUMBER", r"-?\d+(?:\.\d+)?"),
        ("PLUS", r"\+"),
        ("COLON", r":"),
        ("COMMA", r","),
        ("DOT", r"\."),
        ("LPAREN", r"\("),
        ("RPAREN", r"\)"),
        ("LBRACK", r"\["),
        ("RBRACK", r"\]"),
        ("LBRACE", r"{"),
        ("RBRACE", r"}"),
        ("HYPHEN", r"-"),
        ("PIPE", r"\|"),
        ("GT", r">"),
        ("IDENT", r"[a-zA-Z_][a-zA-Z0-9_]*"),
    ]

    MASTER_RE = re.compile(
        "|".join(f"(?P<{name}>{pattern})" for name, pattern in TOKEN_SPEC)
    )

    def __init__(self, source: str):
        self.source = source
        self.pos = 0
        self.lineno = 1
        self.tokens: list[Token] = []
        self._tokenize()

    def _tokenize(self):
        while self.pos < len(self.source):
            m = self.MASTER_RE.match(self.source, self.pos)
            if not m:
                char = self.source[self.pos]
                if char.isspace():
                    if char == "\n":
                        self.lineno += 1
                    self.pos += 1
                    continue
                raise DatarSyntaxError(
                    f"Unexpected character: '{char}'", lineno=self.lineno
                )
            kind = m.lastgroup
            value = m.group()
            if kind == "WHITESPACE":
                pass
            elif kind == "NEWLINE":
                self.lineno += 1
            elif kind == "COMMENT":
                pass
            elif kind == "STRING":
                # Keep the raw string including quotes; parsing later will handle escapes.
                self.tokens.append(Token(TokenType.STRING, value, self.lineno))
            elif kind == "NUMBER":
                if "." in value:
                    val = float(value)
                else:
                    val = int(value)
                self.tokens.append(Token(TokenType.NUMBER, str(val), self.lineno))
            elif kind == "IDENT":
                self.tokens.append(Token(TokenType.IDENT, value.lower(), self.lineno))
            else:
                # Handle potential None value for kind (though it should never happen with our named groups)
                token_type = kind if kind is not None else "UNKNOWN"
                self.tokens.append(Token(token_type, value, self.lineno))
            self.pos = m.end()
        self.tokens.append(Token(TokenType.EOF, "", self.lineno))

    def __iter__(self) -> Iterator[Token]:
        return iter(self.tokens)
