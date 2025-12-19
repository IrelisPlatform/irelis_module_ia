from __future__ import annotations

from typing import Callable, Iterable

from sqlalchemy import and_, not_, or_
from sqlalchemy.sql.elements import ClauseElement


class BooleanQueryParser:
    """Parse human friendly boolean queries into SQLAlchemy expressions."""

    OPERATORS = {"AND", "OR", "NOT"}
    PRECEDENCE = {"OR": 1, "AND": 2, "NOT": 3}
    RIGHT_ASSOC = {"NOT"}

    def build_expression(
        self,
        query: str,
        term_factory: Callable[[str], ClauseElement | None],
    ) -> ClauseElement | None:
        """Return a SQL expression matching the provided boolean query."""

        tokens = self._tokenize(query)
        if not tokens:
            return None

        normalized_tokens = self._apply_implicit_and(tokens)
        postfix = self._to_postfix(normalized_tokens)
        return self._postfix_to_expression(postfix, term_factory)

    def _tokenize(self, query: str) -> list[str]:
        """Split the query into keywords, operators, and parentheses."""

        if not query:
            return []

        tokens: list[str] = []
        length = len(query)
        index = 0

        while index < length:
            char = query[index]

            if char.isspace():
                index += 1
                continue

            if char == '"':
                phrase, index = self._consume_phrase(query, index + 1)
                tokens.append(phrase)
                continue

            if char in "()":
                tokens.append(char)
                index += 1
                continue

            if char == "-" and self._is_minus_operator(query, index):
                tokens.append("NOT")
                index += 1
                continue

            start = index
            while index < length and not query[index].isspace() and query[index] not in "()\"":
                if query[index] == "-" and self._is_minus_operator(query, index):
                    break
                index += 1

            if start == index:
                # Should not happen, but guard against infinite loops
                index += 1
                continue

            word = query[start:index]
            upper_word = word.upper()
            if upper_word in self.OPERATORS:
                tokens.append(upper_word)
            else:
                tokens.append(word)

        return tokens

    def _consume_phrase(self, query: str, index: int) -> tuple[str, int]:
        """Consume a quoted expression starting at the given index."""

        length = len(query)
        phrase_chars: list[str] = []
        while index < length:
            char = query[index]
            if char == '"':
                return "".join(phrase_chars), index + 1
            phrase_chars.append(char)
            index += 1
        raise ValueError("Guillemets non fermés dans la requête.")

    def _is_minus_operator(self, query: str, index: int) -> bool:
        """Return True when '-' acts as the NOT operator."""

        if query[index] != "-":
            return False

        prev_char = query[index - 1] if index > 0 else " "
        next_char = query[index + 1] if index + 1 < len(query) else ""

        if not next_char or next_char.isspace() or next_char == ")":
            return False

        if not prev_char.isspace() and prev_char not in "(":
            return False

        return True

    def _apply_implicit_and(self, tokens: Iterable[str]) -> list[str]:
        """Insert explicit AND operators where the user omitted them."""

        normalized: list[str] = []
        prev_type: str | None = None

        for token in tokens:
            current_type = self._token_type(token)
            if (
                normalized
                and prev_type in {"TERM", ")"}
                and (current_type in {"TERM", "("} or token == "NOT")
            ):
                normalized.append("AND")

            if token.upper() in self.OPERATORS:
                normalized.append(token.upper())
            else:
                normalized.append(token)

            prev_type = current_type

        return normalized

    def _token_type(self, token: str) -> str:
        if token == "(":
            return "("
        if token == ")":
            return ")"
        if token.upper() in self.OPERATORS:
            return "OP"
        return "TERM"

    def _to_postfix(self, tokens: Iterable[str]) -> list[str]:
        """Convert infix tokens to postfix (Reverse Polish) notation."""

        output: list[str] = []
        stack: list[str] = []

        for token in tokens:
            upper_token = token.upper()

            if upper_token in self.OPERATORS:
                while (
                    stack
                    and stack[-1].upper() in self.OPERATORS
                    and (
                        self.PRECEDENCE[stack[-1].upper()] > self.PRECEDENCE[upper_token]
                        or (
                            self.PRECEDENCE[stack[-1].upper()] == self.PRECEDENCE[upper_token]
                            and upper_token not in self.RIGHT_ASSOC
                        )
                    )
                ):
                    output.append(stack.pop())
                stack.append(upper_token)
            elif token == "(":
                stack.append(token)
            elif token == ")":
                found_left = False
                while stack:
                    top = stack.pop()
                    if top == "(":
                        found_left = True
                        break
                    output.append(top)
                if not found_left:
                    raise ValueError("Parenthèses non équilibrées dans la requête.")
            else:
                output.append(token)

        while stack:
            top = stack.pop()
            if top in {"(", ")"}:
                raise ValueError("Parenthèses non équilibrées dans la requête.")
            output.append(top)

        return output

    def _postfix_to_expression(
        self,
        postfix: Iterable[str],
        term_factory: Callable[[str], ClauseElement | None],
    ) -> ClauseElement | None:
        """Construct the SQLAlchemy expression from postfix tokens."""

        stack: list[ClauseElement] = []

        for token in postfix:
            upper_token = token.upper()
            if upper_token not in self.OPERATORS:
                clause = term_factory(token)
                if clause is not None:
                    stack.append(clause)
                continue

            if upper_token == "NOT":
                if not stack:
                    raise ValueError("L'opérateur NOT doit précéder un terme ou un groupe.")
                operand = stack.pop()
                stack.append(not_(operand))
                continue

            if len(stack) < 2:
                raise ValueError("Expression booléenne invalide.")

            right = stack.pop()
            left = stack.pop()
            if upper_token == "AND":
                stack.append(and_(left, right))
            else:
                stack.append(or_(left, right))

        if not stack:
            return None

        expression = stack.pop()
        while stack:
            expression = and_(stack.pop(), expression)

        return expression


__all__ = ["BooleanQueryParser"]
