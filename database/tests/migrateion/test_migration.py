from migration.command import Command
from native import get_all_tables, get_connection


def test_alembic_command() -> None:
    cmd = Command(conn_url="mysql+pymysql://root:root@localhost/study_python")
    cmd.reset()

    conn = get_connection()

    tables = get_all_tables(conn)
    assert {
        "alembic_version",
        "core_groups",
        "core_users",
        "core_user_groups",
    }.issubset(set(tables))
