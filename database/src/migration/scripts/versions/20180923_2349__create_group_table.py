"""_create group table

Revision ID: 20180923_2349
Revises: 20180923_1959
Create Date: 2018-09-23 23:50:00.465304

"""
from typing import Optional

import sqlalchemy as sa
from alembic import op
from sqlalchemy import BIGINT, TIMESTAMP, VARCHAR, func, text

# revision identifiers, used by Alembic.
revision = "20180923_2349"
down_revision = "20180923_1959"
branch_labels: Optional[str] = None
depends_on: Optional[str] = None


def upgrade() -> None:
    op.create_table(
        "core_groups",
        sa.Column("id", BIGINT(), primary_key=True, autoincrement=True),
        sa.Column("name", VARCHAR(50), nullable=False),
        sa.Column("created_at", TIMESTAMP, nullable=False, server_default=func.now()),
        sa.Column(
            "updated_at",
            TIMESTAMP,
            nullable=False,
            server_default=text("CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP"),
        ),
    )
    op.create_index("ux_name", table_name="core_groups", columns=["name"], unique=True)


def downgrade() -> None:
    op.drop_index("ux_name", table_name="core_groups")
    op.drop_table("core_groups")
