from typing import TypeVar, Union

from sqlalchemy import Table
from sqlalchemy.orm import FromStatement
from sqlalchemy.sql import CompoundSelect, Executable, Select

Statement = TypeVar(
    "Statement", bound=Union[Select, FromStatement, CompoundSelect, Executable]
)


def soft_delete_rewriter(stmt: Statement) -> Statement:
    if not isinstance(stmt, Select):
        return stmt

    if stmt.get_execution_options().get("with_deleted"):
        return stmt

    for from_obj in stmt.get_final_froms():
        if not isinstance(from_obj, Table):
            continue

        column_obj = from_obj.columns.get("deleted")
        if column_obj is None:
            continue

        stmt = stmt.where(column_obj == 0)

    return stmt
