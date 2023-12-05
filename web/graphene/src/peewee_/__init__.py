from peewee import PostgresqlDatabase

from .core import context, make_cursor, parse_cursor, pg_db
from .models import Department as DepartmentModel
from .models import Employee as EmployeeModel
from .models import Gender as GenderModel
from .models import Org as OrgModel
from .models import Role as RoleModel
from .schemas import schema
from .utils import initialize_tables

__all__ = [
    "context",
    "make_cursor",
    "parse_cursor",
    "pg_db",
    "DepartmentModel",
    "EmployeeModel",
    "GenderModel",
    "OrgModel",
    "RoleModel",
    "schema",
    "initialize_tables",
]

pg_db.initialize(
    PostgresqlDatabase(
        database="study_python_graphene",
        host="localhost",
        port=5432,
        user="root",
        password="password",
    )
)
