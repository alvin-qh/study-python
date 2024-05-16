"""_create user group table

Revision ID: 20180923_2354
Revises: 20180923_2349
Create Date: 2018-09-23 23:54:14.880453

"""
import sqlalchemy as sa
from alembic import op
from sqlalchemy import BIGINT, TIMESTAMP, func, text

# revision identifiers, used by Alembic.
revision = "20180923_2354"
down_revision = "20180923_2349"
branch_labels = None
depends_on = None


def upgrade():
    op.create_table(
        "user_group",
        sa.Column("id", BIGINT(), primary_key=True, autoincrement=True),
        sa.Column("user_id", BIGINT(), nullable=False),
        sa.Column("group_id", BIGINT(), nullable=False),
        sa.Column("created_at", TIMESTAMP, nullable=False, server_default=func.now()),
        sa.Column(
            "updated_at",
            TIMESTAMP,
            nullable=False,
            server_default=text("CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP"),
        ),
    )
    op.create_index(
        "ux_user_group_id",
        table_name="user_group",
        columns=["user_id", "group_id"],
        unique=True,
    )


def downgrade():
    op.drop_index("ux_user_group_id", table_name="user_group")
    op.drop_table("user_group")
