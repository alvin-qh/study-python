from .core import context, make_cursor, mongodb, parse_cursor
from .models import Department as DepartmentModel
from .models import Employee as EmployeeModel
from .models import Gender as GenderModel
from .models import Org as OrgModel
from .models import Role as RoleModel
from .schemas import schema
from .utils import clear_db, ensure_indexes

__all__ = [
    "context",
    "make_cursor",
    "parse_cursor",
    "DepartmentModel",
    "EmployeeModel",
    "GenderModel",
    "OrgModel",
    "RoleModel",
    "schema",
    "clear_db",
    "ensure_indexes",
]

mongodb.connect(
    dbname="study_python_graphene",
    host="127.0.0.1",
    port=27017,
    username="root",
    password="password",
)
