import signal

from peewee import SqliteDatabase

# 实例化数据库连接
db = SqliteDatabase(
    database=":memory:",
)

# 监听系统信号, 当系统退出时关闭数据库连接
signal.signal(signal.SIGHUP, lambda sig, frame: db.close())
