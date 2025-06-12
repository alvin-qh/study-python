from .core import context, mongodb
from .models import Department, Employee, Gender, Org, Role
from .utils import clear_db, ensure_indexes, run_once

__all__ = [
    "context",
    "mongodb",
    "Org",
    "Department",
    "Employee",
    "Gender",
    "Role",
    "clear_db",
    "ensure_indexes",
    "run_once",
]

# 连接数据库
mongodb.connect(
    dbname="study_python_mongo",
    host="127.0.0.1",
    port=27017,
    replicaSet="rs0",
    directConnection=True,
    # username="root",
    # password="password",
)
