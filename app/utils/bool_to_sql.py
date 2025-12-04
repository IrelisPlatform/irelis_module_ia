from __future__ import annotations

from dataclasses import dataclass
from typing import Dict, List, Optional, Sequence, Tuple

from sqlalchemy.sql import text

from app.utils.bool_parser import (
    And,
    Field,
    Node,
    Not,
    Or,
    Phrase,
    Term,
    Parser,
    tokenize,
)


@dataclass(frozen=True)
class SqlTarget:
    """
    Décrit comment chercher une valeur.
    - kind = 'column'  -> colonne sur la table candidates
    - kind = 'related' -> EXISTS sur une table reliée (skills, languages, experiences, ...)
    """

    kind: str
    column: Optional[str] = None  # utilisé pour column et related
    table: Optional[str] = None  # utilisé pour related
    fk: Optional[str] = None  # nom de la colonne FK vers candidates.id pour related


CANDIDATES_TABLE = "candidates"
CANDIDATE_ID_COL = "id"


DEFAULT_TARGETS: Sequence[SqlTarget] = (
    SqlTarget(kind="column", column="first_name"),
    SqlTarget(kind="column", column="last_name"),
    SqlTarget(kind="column", column="professional_title"),
    SqlTarget(kind="column", column="presentation"),
    SqlTarget(kind="column", column="city"),
    SqlTarget(kind="column", column="country"),
)

FIELD_TARGETS: dict[str, Sequence[SqlTarget]] = {
    "firstname": (SqlTarget(kind="column", column="first_name"),),
    "lastname": (SqlTarget(kind="column", column="last_name"),),
    "name": (
        SqlTarget(kind="column", column="first_name"),
        SqlTarget(kind="column", column="last_name"),
    ),
    "title": (SqlTarget(kind="column", column="professional_title"),),
    "city": (SqlTarget(kind="column", column="city"),),
    "country": (SqlTarget(kind="column", column="country"),),
    "skill": (
        SqlTarget(
            kind="related", table="skill", fk="candidate_id", column="name"
        ),
    ),
    "skills": (
        SqlTarget(
            kind="related", table="skill", fk="candidate_id", column="name"
        ),
    ),
    "language": (
        SqlTarget(
            kind="related", table="language", fk="candidate_id", column="language"
        ),
    ),
    "languages": (
        SqlTarget(
            kind="related", table="language", fk="candidate_id", column="language"
        ),
    ),
    "experience": (
        SqlTarget(
            kind="related", table="experience", fk="candidate_id", column="position"
        ),
        SqlTarget(
            kind="related", table="experience", fk="candidate_id", column="company_name"
        ),
        SqlTarget(
            kind="related", table="experience", fk="candidate_id", column="description"
        ),
    ),
}


def to_ilike_pattern(value: str) -> str:
    """
    Convertit un terme/phrase avec * en pattern ILIKE PostgreSQL.
    - On remplace * par %.
    - Si pas de wildcard explicite, on fait un 'contient'.
    """
    if "*" in value:
        return value.replace("*", "%")
    return f"%{value}%"


class SqlBuilder:
    """
    Visiteur de l'AST -> (sql, params)
    Gère la propagation d'un 'champ courant' (ctx_field) pour Field(expr).
    """

    def __init__(self):
        self.params: List[Tuple[str, str]] = []

    def build_where(self, ast: Node) -> Tuple[str, Dict[str, str]]:
        sql = self._visit(ast, ctx_field=None)
        return sql, dict(self.params)

    def _new_param(self, value: str) -> str:
        key = f"p{len(self.params)}"
        self.params.append((key, value))
        return key

    def _visit(self, node: Node, ctx_field: Optional[str]) -> str:
        if isinstance(node, Term):
            return self._visit_term(node, ctx_field)
        if isinstance(node, Phrase):
            return self._visit_phrase(node, ctx_field)
        if isinstance(node, Field):
            return self._visit_field(node)
        if isinstance(node, And):
            return self._visit_and(node, ctx_field)
        if isinstance(node, Or):
            return self._visit_or(node, ctx_field)
        if isinstance(node, Not):
            return self._visit_not(node, ctx_field)
        raise TypeError(f"Nœud inconnu: {type(node)}")

    def _targets_for_field(self, field: Optional[str]) -> Sequence[SqlTarget]:
        if field is None:
            return DEFAULT_TARGETS
        return FIELD_TARGETS.get(field.lower(), DEFAULT_TARGETS)

    def _term_sql_over_targets(
        self, term_pattern: str, targets: Sequence[SqlTarget]
    ) -> str:
        parts: List[str] = []
        for target in targets:
            param = self._new_param(term_pattern)
            if target.kind == "column":
                column = target.column
                if not column:
                    raise ValueError("Column target sans colonne")
                parts.append(f'{CANDIDATES_TABLE}."{column}" ILIKE :{param}')
            elif target.kind == "related":
                table = target.table
                fk = target.fk
                column = target.column
                if not (table and fk and column):
                    raise ValueError("Related target mal configuré")
                alias = f"{table}_{param}"
                parts.append(
                    f"""EXISTS (
                            SELECT 1 FROM {table} {alias}
                            WHERE {alias}."{fk}" = {CANDIDATES_TABLE}."{CANDIDATE_ID_COL}"
                              AND {alias}."{column}" ILIKE :{param}
                        )"""
                )
            else:
                raise ValueError(f"Target kind inconnu: {target.kind}")
        if len(parts) == 1:
            return parts[0]
        return "(" + " OR ".join(parts) + ")"

    def _visit_term(self, node: Term, ctx_field: Optional[str]) -> str:
        pattern = to_ilike_pattern(node.value)
        targets = self._targets_for_field(ctx_field)
        return self._term_sql_over_targets(pattern, targets)

    def _visit_phrase(self, node: Phrase, ctx_field: Optional[str]) -> str:
        pattern = to_ilike_pattern(node.value)
        targets = self._targets_for_field(ctx_field)
        return self._term_sql_over_targets(pattern, targets)

    def _visit_field(self, node: Field) -> str:
        fld = node.field.lower()
        val = node.value
        if isinstance(val, (Term, Phrase)):
            pattern = to_ilike_pattern(val.value)
            targets = self._targets_for_field(fld)
            return self._term_sql_over_targets(pattern, targets)
        return self._visit(val, ctx_field=fld)

    def _visit_and(self, node: And, ctx_field: Optional[str]) -> str:
        parts = [self._visit(child, ctx_field) for child in node.children]
        if not parts:
            return "TRUE"
        return "(" + " AND ".join(parts) + ")"

    def _visit_or(self, node: Or, ctx_field: Optional[str]) -> str:
        parts = [self._visit(child, ctx_field) for child in node.children]
        if not parts:
            return "FALSE"
        return "(" + " OR ".join(parts) + ")"

    def _visit_not(self, node: Not, ctx_field: Optional[str]) -> str:
        inner = self._visit(node.child, ctx_field)
        return f"(NOT {inner})"


def build_boolean_filter(query_text: str) -> Tuple[str, Dict[str, str]]:
    ast = Parser(tokenize(query_text)).parse()
    return SqlBuilder().build_where(ast)


def boolean_filter_clause(query_text: str):
    """
    Helper qui renvoie une clause SQLAlchemy utilisable dans .filter().
    """
    sql, params = build_boolean_filter(query_text)
    return text(sql).params(**params)
