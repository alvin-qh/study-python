from migration.command import Command
from mysql import get_all_tables
from pymysql import connect  # type: ignore[import-untyped]
from pymysql.cursors import DictCursor  # type: ignore[import-untyped]


def test_alembic_command() -> None:
    cmd = Command(conn_url="mysql+pymysql://root:root@localhost/study_python_alembic")
    cmd.reset()

    conn = connect(
        host="127.0.0.1",
        port=3306,
        db="study_python_alembic",
        user="root",
        password="root",
        cursorclass=DictCursor,
    )

    tables = get_all_tables(conn)
    assert {
        "alembic_version",
        "group",
        "user",
        "user_group",
    }.issubset(set(tables))
