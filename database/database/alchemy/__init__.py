from .core import session, soft_deleted_select
from .model import Gender, Group, User, UserGroup

__all__ = [
    "session",
    "soft_deleted_select",
    "initialize_tables",
    "Gender",
    "Group",
    "User",
    "UserGroup",
]


def initialize_tables() -> None:
    from .core import engine

    for table in [UserGroup, User, Group]:
        try:
            table.__table__.drop(engine)  # type: ignore
        except Exception:
            pass

    for table in [User, Group, UserGroup]:
        table.__table__.create(engine)  # type: ignore

    session.commit()
