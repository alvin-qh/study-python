"""_create tables

Revision ID: 20180923_1624
Revises:
Create Date: 2018-09-23 16:24:34.657226

"""
import sqlalchemy as sa
from alembic import op
from sqlalchemy import BIGINT, CHAR, DATE, TIMESTAMP, VARCHAR, func, text

# revision identifiers, used by Alembic.
revision = "20180923_1624"
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    op.create_table(
        "user",
        sa.Column("id", BIGINT(), primary_key=True, autoincrement=True),
        sa.Column("id_num", VARCHAR(50), nullable=False),
        sa.Column("name", VARCHAR(50), nullable=False),
        sa.Column("gender", CHAR(1), nullable=False),
        sa.Column("birthday", DATE, nullable=True),
        sa.Column("created_at", TIMESTAMP, nullable=False, server_default=func.now()),
        sa.Column(
            "updated_at",
            TIMESTAMP,
            nullable=False,
            server_default=text("CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP"),
        ),
    )
    op.create_index("ux_id_num", table_name="user", columns=["id_num"], unique=True)
    op.create_index("ix_name", table_name="user", columns=["name"], unique=False)


def downgrade():
    op.drop_index("ux_id_num", table_name="user")
    op.drop_table("user")
