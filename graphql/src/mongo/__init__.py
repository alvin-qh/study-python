from .core import mongodb
from .models import Department as DepartmentModel
from .models import Employee as EmployeeModel
from .models import Gender as GenderModel
from .models import Org as OrgModel
from .models import Role as RoleModel
from .utils import make_cursor, parse_cursor

__all__ = [
    "mongodb",
    "DepartmentModel",
    "EmployeeModel",
    "GenderModel",
    "OrgModel",
    "RoleModel",
    "make_cursor",
    "parse_cursor",
]

mongodb.connect(
    dbname="study_python_graphene",
    host="127.0.0.1",
    port=27017,
    username="root",
    password="password",
)
