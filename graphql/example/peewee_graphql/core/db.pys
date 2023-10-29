import signal

from peewee import PostgresqlDatabase

db = PostgresqlDatabase(
    database="study_python",
    host="localhost",
    port=5432,
    user="root",
    password="password"
)

signal.signal(signal.SIGHUP, lambda: db.close())
