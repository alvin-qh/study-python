from functools import wraps
from typing import Callable

from flask import request
from flask_sqlalchemy import SQLAlchemy
from werkzeug.local import Local, release_local

# db = SQLAlchemy(engine_options=dict(echo=False))
db = SQLAlchemy()


def init_app(app) -> None:
    """
    初始化数据库连接
    """
    from models import Group, User, UserGroup

    db.init_app(app)  # 初始化数据库连接
    db.app = app

    # Only for mysql
    #
    # @listens_for(Pool, "checkout")
    # def checkout_listener(dbapi_con, con_record, con_proxy):
    #     try:
    #         try:
    #             dbapi_con.ping(False)
    #         except TypeError:
    #             dbapi_con.ping()
    #     except dbapi_con.OperationalError as exc:
    #         if exc.args[0] in {2006, 2013, 2014, 2045, 2055}:
    #             raise DisconnectionError()
    #         raise

    @app.teardown_request
    def tear_down(exception=None) -> None:
        """
        请求结束后处理
        """
        if request.url_rule and request.url_rule.endpoint != "static":
            if db.session:
                # 删除当前 session，回归连接池
                db.session.remove()

    # 创建所需的表
    for table in [User, Group, UserGroup]:
        try:
            table.__table__.create(db.engine)
            db.session.commit()
        except:
            pass


TRANSACTION_ATTR_NAME = "_transaction_begin_"

local = Local()


def transaction(callback=None) -> Callable:
    """
    处理事务的装饰器
    """
    def decorator(f):
        @wraps(f)
        def decorated_function(*args, **kwargs):
            sp = hasattr(local, TRANSACTION_ATTR_NAME)
            if not sp:
                setattr(local, TRANSACTION_ATTR_NAME, True)

            try:
                rt = f(*args, **kwargs)
                if not sp:
                    db.session.commit()
                    if callback:
                        callback()
                return rt
            except:
                if not sp:
                    db.session.rollback()
                raise
            finally:
                if not sp:
                    release_local(local)

        return decorated_function

    return decorator
