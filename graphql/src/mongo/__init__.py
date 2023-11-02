from .core import mongodb

__all__ = ["mongodb"]

mongodb.connect(
    dbname="graphene",
    host="127.0.0.1",
    port=27017,
    user="root",
    password="password",
)
