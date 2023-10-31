from .core import session

__all__ = [
    "session",
    "initialize_tables",
]


def initialize_tables():
    from sqlalchemy import text

    from .core import engine
    from .model import Group, User, UserGroup

    for table in [User, Group, UserGroup]:
        try:
            table.__table__.create(engine)
            session.commit()
        except Exception:
            pass

        session.execute(text(f"DELETE FROM {table.__tablename__}"))
        session.commit()
