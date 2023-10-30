from .model import session

__all__ = [
    "session",
    "initialize_tables",
]


def initialize_tables():
    from sqlalchemy import text

    from .model import Group, User, UserGroup, engine, session

    for table in [User, Group, UserGroup]:
        try:
            table.__table__.create(engine)
            session.commit()
        except Exception:
            pass

        session.execute(text(f"DELETE FROM {table.__tablename__}"))
        session.commit()
