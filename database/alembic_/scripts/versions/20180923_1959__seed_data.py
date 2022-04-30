"""_seed data

Revision ID: 20180923_1959
Revises: 20180923_1656
Create Date: 2018-09-23 19:59:19.527802

"""
from alembic import op
from sqlalchemy import column, table
from sqlalchemy.orm import Session

# revision identifiers, used by Alembic.
revision = "20180923_1959"
down_revision = "20180923_1624"
branch_labels = None
depends_on = None


def upgrade():
    core_user = table("core_users",
                      column("id_num"),
                      column("name"),
                      column("gender"),
                      column("birthday"))

    session = Session(bind=op.get_bind())
    op.execute(core_user
               .insert()
               .values(id_num="61010419810303210X",
                       name="Alvin",
                       gender="M",
                       birthday="1981-03-03"))
    session.commit()


def downgrade():
    core_user = table("core_users", column("id_num"))

    session = Session(bind=op.get_bind())
    op.execute(core_user
               .delete()
               .where(core_user.c.id_num == "61010419810303210X"))
    session.commit()
