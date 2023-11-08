import signal

from peewee import PostgresqlDatabase

# 创建 pg 数据库连接
pg_db = PostgresqlDatabase(
    database="study_python_graphene",
    host="localhost",
    port=5432,
    user="root",
    password="password",
)

# 监听系统关闭信号, 同时关闭数据库
signal.signal(signal.SIGHUP, lambda sig, frame: pg_db.close())
