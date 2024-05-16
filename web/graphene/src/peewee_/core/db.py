import signal

from peewee import Proxy

# 创建 pg 数据库连接
pg_db = Proxy()

# 监听系统关闭信号, 同时关闭数据库
signal.signal(signal.SIGHUP, lambda sig, frame: pg_db.close())
