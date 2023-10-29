"""baseline

Revision ID: 8185439e9008
Revises:
Create Date: 2021-05-24 23:00:41.255353

"""
from typing import Optional

from alembic import op
from sqlalchemy.sql import text

# revision identifiers, used by Alembic.

revision = "8185439e9008"
down_revision: Optional[str] = None
branch_labels: Optional[str] = None
depends_on: Optional[str] = None


def upgrade():
    conn = op.get_bind()
    conn.execute(text("""\
create table if not exists gql_org(
    id bigserial not null constraint gql_org_pk primary key,
    name varchar not null constraint gql_org_name_ux unique,
    created_at timestamp default now(),
    updated_at timestamp
);

create table if not exists gql_department(
    id bigserial not null constraint gql_department_pk primary key,
    org_id bigint not null constraint gql_department_org_fk references gql_org(id),
    name varchar not null constraint gql_department_name_ux unique,
    level integer not null default 0,
    manager_id bigint,
    created_at timestamp default now(),
    updated_at timestamp,
    created_by bigint,
    updated_by bigint
);

create table if not exists gql_role(
    id bigserial not null constraint gql_role_pk primary key,
    org_id bigint not null constraint gql_role_org_fk references gql_org(id),
    name varchar not null constraint gql_role_name_ux unique,
    created_at timestamp default now(),
    updated_at timestamp
);

create table if not exists gql_employee(
    id bigserial not null constraint gql_employee_pk primary key,
    org_id bigint not null constraint gql_employee_org_fk references gql_org(id),
    name varchar not null,
    gender char(1) not null default 'M',
    department_id bigint not null constraint gql_employee_department_fk references gql_department(id),
    role_id bigint not null constraint gql_employee_role_fk references gql_role(id),
    created_at timestamp default now(),
    updated_at timestamp,
    created_by bigint,
    updated_by bigint
);


alter table gql_department add constraint gql_department_manager_fk foreign key(manager_id) references gql_employee(id)
"""))


def downgrade():
    conn = op.get_bind()
    conn.execute(text("""\
alter table if exists gql_employee drop constraint if exists gql_employee_department_fk;
alter table if exists gql_employee drop constraint if exists gql_employee_role_fk;
alter table if exists gql_department drop constraint if exists gql_department_manager_fk;

drop table if exists gql_employee;
drop table if exists gql_role;
drop table if exists gql_department;
drop table if exists gql_org;
"""))
