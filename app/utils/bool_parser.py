from __future__ import annotations

from dataclasses import dataclass
from typing import Iterator, List, Optional, Tuple
import re

# ============
# AST NODES
# ============


@dataclass(frozen=True)
class Node:
    ...


@dataclass(frozen=True)
class Term(Node):
    value: str


@dataclass(frozen=True)
class Phrase(Node):
    value: str  # sans guillemets


@dataclass(frozen=True)
class Field(Node):
    field: str
    value: Node  # Term | Phrase | (AND/OR tree)


@dataclass(frozen=True)
class Not(Node):
    child: Node


@dataclass(frozen=True)
class And(Node):
    children: List[Node]


@dataclass(frozen=True)
class Or(Node):
    children: List[Node]


# ============
# TOKENIZER
# ============
Token = Tuple[str, str]  # (type, value)

KEYWORDS = {"AND", "OR", "NOT"}

# Identifiant de terme/champ : lettres, chiffres, _, -, ., /, *
IDENT_RE = re.compile(r"[A-Za-z0-9_\-\./\*]+", re.ASCII)
WS_RE = re.compile(r"\s+")


def tokenize(query: str) -> List[Token]:
    tokens: List[Token] = []
    i, n = 0, len(query)
    while i < n:
        # espaces
        m = WS_RE.match(query, i)
        if m:
            i = m.end()
            continue

        ch = query[i]

        # parenthèses
        if ch == "(":
            tokens.append(("LPAREN", ch))
            i += 1
            continue
        if ch == ")":
            tokens.append(("RPAREN", ch))
            i += 1
            continue

        # guillemets => phrase
        if ch == '"':
            j = i + 1
            buf = []
            while j < n and query[j] != '"':
                buf.append(query[j])
                j += 1
            if j >= n:
                raise ValueError("Phrase non fermée avec '\"'")
            tokens.append(("PHRASE", "".join(buf)))
            i = j + 1
            continue

        # deux-points (pour field:)
        if ch == ":":
            tokens.append(("COLON", ch))
            i += 1
            continue

        # mot-clé / ident
        m = IDENT_RE.match(query, i)
        if m:
            raw = m.group(0)
            t = raw.upper()
            if t in KEYWORDS:
                tokens.append((t, raw))
            else:
                tokens.append(("IDENT", raw))
            i = m.end()
            continue

        raise ValueError(f"Caractère inattendu à la position {i}: {ch!r}")

    tokens.append(("EOF", ""))
    return tokens


# ============
# PARSER (RD)
# ============


class Parser:
    def __init__(self, tokens: List[Token]):
        self.tokens = tokens
        self.pos = 0

    def peek(self) -> Token:
        return self.tokens[self.pos]

    def eat(self, *expected: str) -> Token:
        tok = self.peek()
        if expected and tok[0] not in expected:
            raise ValueError(f"Attendu {expected} mais obtenu {tok}")
        self.pos += 1
        return tok

    def parse(self) -> Node:
        node = self.parse_or()
        if self.peek()[0] != "EOF":
            raise ValueError(f"Tokens restants après fin de parse: {self.peek()}")
        return node

    # expr := or_expr
    def parse_or(self) -> Node:
        left = self.parse_and()
        ors: List[Node] = [left]
        while self.peek()[0] == "OR":
            self.eat("OR")
            right = self.parse_and()
            ors.append(right)
        if len(ors) == 1:
            return left
        return Or(ors)

    # and_expr := unary (AND unary)*
    def parse_and(self) -> Node:
        left = self.parse_unary()
        ands: List[Node] = [left]
        while self.peek()[0] == "AND":
            self.eat("AND")
            right = self.parse_unary()
            ands.append(right)
        if len(ands) == 1:
            return left
        return And(ands)

    # unary := NOT unary | primary
    def parse_unary(self) -> Node:
        if self.peek()[0] == "NOT":
            self.eat("NOT")
            child = self.parse_unary()
            return Not(child)
        return self.parse_primary()

    # primary := factor | '(' expr ')'
    def parse_primary(self) -> Node:
        if self.peek()[0] == "LPAREN":
            self.eat("LPAREN")
            node = self.parse_or()
            self.eat("RPAREN")
            return node
        return self.parse_factor()

    # factor := field_factor | term
    def parse_factor(self) -> Node:
        if self.peek()[0] == "IDENT":
            save = self.pos
            ident = self.eat("IDENT")[1]
            if self.peek()[0] == "COLON":
                self.eat("COLON")
                if self.peek()[0] == "PHRASE":
                    value = Phrase(self.eat("PHRASE")[1])
                elif self.peek()[0] == "IDENT":
                    value = Term(self.eat("IDENT")[1])
                elif self.peek()[0] == "LPAREN":
                    self.eat("LPAREN")
                    value = self.parse_or()
                    self.eat("RPAREN")
                else:
                    raise ValueError(f"Valeur de champ invalide: {self.peek()}")
                return Field(field=ident, value=value)
            else:
                return Term(ident)
        if self.peek()[0] == "PHRASE":
            return Phrase(self.eat("PHRASE")[1])

        raise ValueError(f"Facteur invalide: {self.peek()}")
