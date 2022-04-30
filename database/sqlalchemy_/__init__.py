from .model import Session

session = Session()


def initialize_tables():
    from .model import Group, User, UserGroup, engine

    for table in [User, Group, UserGroup]:
        try:
            table.__table__.create(engine)
            session.commit()
        except Exception:
            pass

        session.execute('DELETE FROM {}'.format(table.__tablename__))
        session.commit()
