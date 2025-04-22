"""enum roles

Revision ID: a80e58f00f4c
Revises: 1fcb06ab8cff
Create Date: 2025-04-11 22:34:51.821437

"""

import uuid
from datetime import datetime, timezone
from typing import Sequence, Union

import sqlalchemy as sa
from sqlalchemy import TIMESTAMP, UUID, Boolean, String, column, table
from sqlalchemy.dialects import postgresql

from alembic import op

# revision identifiers, used by Alembic.
revision: str = "a80e58f00f4c"
down_revision: Union[str, None] = "1fcb06ab8cff"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    op.drop_constraint("fk_profiles_role_id_roles", "profiles", type_="foreignkey")
    op.drop_column("profiles", "role_id")
    op.drop_table("roles")
    op.execute("CREATE TYPE role AS ENUM ('BASIC', 'SUBSCRIBER', 'ADMIN')")
    op.add_column(
        "profiles",
        sa.Column("role", sa.Enum("BASIC", "SUBSCRIBER", "ADMIN", name="role"), nullable=False),
    )


def downgrade() -> None:
    """Downgrade schema."""
    op.drop_column("profiles", "role")
    op.execute("DROP TYPE role")
    op.create_table(
        "roles",
        sa.Column("id", sa.UUID(), autoincrement=False, nullable=False),
        sa.Column(
            "created_at",
            postgresql.TIMESTAMP(timezone=True),
            autoincrement=False,
            nullable=False,
        ),
        sa.Column("title", sa.VARCHAR(), autoincrement=False, nullable=False),
        sa.Column("system_role", sa.BOOLEAN(), autoincrement=False, nullable=True),
        sa.PrimaryKeyConstraint("id", name="pk_roles"),
        sa.UniqueConstraint("title", name="uq_roles_title"),
    )
    roles_table = table(
        "roles",
        column("id", UUID),
        column("title", String),
        column("system_role", Boolean),
        column("created_at", TIMESTAMP(timezone=True)),
    )
    op.bulk_insert(
        roles_table,
        [
            {
                "id": str(uuid.uuid4()),
                "title": "basic",
                "system_role": False,
                "created_at": datetime.now(timezone.utc),
            },
            {
                "id": str(uuid.uuid4()),
                "title": "subscriber",
                "system_role": False,
                "created_at": datetime.now(timezone.utc),
            },
            {
                "id": str(uuid.uuid4()),
                "title": "admin",
                "system_role": True,
                "created_at": datetime.now(timezone.utc),
            },
        ],
    )
    op.add_column("profiles", sa.Column("role_id", sa.UUID(), autoincrement=False, nullable=True))
    op.create_foreign_key(
        "fk_profiles_role_id_roles",
        "profiles",
        "roles",
        ["role_id"],
        ["id"],
        ondelete="SET NULL",
    )
