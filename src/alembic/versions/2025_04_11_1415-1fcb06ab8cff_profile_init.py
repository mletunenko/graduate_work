"""Profile init

Revision ID: 1fcb06ab8cff
Revises: 
Create Date: 2025-04-11 14:15:31.677529

"""
import uuid
from datetime import datetime, timezone
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa
from sqlalchemy import column, table, Boolean, TIMESTAMP, String
from sqlalchemy.dialects.postgresql import UUID


# revision identifiers, used by Alembic.
revision: str = '1fcb06ab8cff'
down_revision: Union[str, None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    op.create_table('oauth_providers',
    sa.Column('id', sa.UUID(), nullable=False),
    sa.Column('created_at', sa.TIMESTAMP(timezone=True), nullable=False),
    sa.Column('name', sa.String(), nullable=False),
    sa.PrimaryKeyConstraint('id', name=op.f('pk_oauth_providers')),
    sa.UniqueConstraint('name', name=op.f('uq_oauth_providers_name'))
    )
    op.create_table('roles',
    sa.Column('id', sa.UUID(), nullable=False),
    sa.Column('created_at', sa.TIMESTAMP(timezone=True), nullable=False),
    sa.Column('title', sa.String(), nullable=False),
    sa.Column('system_role', sa.Boolean(), nullable=True),
    sa.PrimaryKeyConstraint('id', name=op.f('pk_roles')),
    sa.UniqueConstraint('title', name=op.f('uq_roles_title'))
    )
    roles_table = table(
        "roles",
        column("id", UUID),
        column("title", String),
        column("system_role", Boolean),
        column("created_at", TIMESTAMP(timezone=True)),
    )
    op.bulk_insert(roles_table, [
        {"id": str(uuid.uuid4()), "title": "subscriber", "system_role": False, "created_at": datetime.now(timezone.utc)},
        {"id": str(uuid.uuid4()), "title": "admin", "system_role": True, "created_at": datetime.now(timezone.utc)},
    ])
    op.create_table('profiles',
    sa.Column('id', sa.UUID(), nullable=False),
    sa.Column('created_at', sa.TIMESTAMP(timezone=True), nullable=False),
    sa.Column('updated_at', sa.TIMESTAMP(timezone=True), nullable=False),
    sa.Column('email', sa.String(), nullable=False),
    sa.Column('phone', sa.String(), nullable=False),
    sa.Column('first_name', sa.String(), nullable=False),
    sa.Column('last_name', sa.String(), nullable=False),
    sa.Column('birth_date', sa.Date(), nullable=False),
    sa.Column('role_id', sa.UUID(), nullable=True),
    sa.ForeignKeyConstraint(['role_id'], ['roles.id'], name=op.f('fk_profiles_role_id_roles'), ondelete='SET NULL'),
    sa.PrimaryKeyConstraint('id', name=op.f('pk_profiles')),
    sa.UniqueConstraint('email', name=op.f('uq_profiles_email')),
    sa.UniqueConstraint('phone', name=op.f('uq_profiles_phone'))
    )
    op.create_table('oauth_accounts',
    sa.Column('id', sa.UUID(), nullable=False),
    sa.Column('created_at', sa.TIMESTAMP(timezone=True), nullable=False),
    sa.Column('profile_id', sa.UUID(), nullable=False),
    sa.Column('provider_id', sa.UUID(), nullable=False),
    sa.Column('provider_user_id', sa.String(), nullable=True, comment='user id предоставляемый провайдером oauth'),
    sa.Column('access_token', sa.String(), nullable=True),
    sa.Column('refresh_token', sa.String(), nullable=True),
    sa.Column('expires_at', sa.Integer(), nullable=True),
    sa.ForeignKeyConstraint(['profile_id'], ['profiles.id'], name=op.f('fk_oauth_accounts_profile_id_profiles'), ondelete='CASCADE'),
    sa.ForeignKeyConstraint(['provider_id'], ['oauth_providers.id'], name=op.f('fk_oauth_accounts_provider_id_oauth_providers'), ondelete='CASCADE'),
    sa.PrimaryKeyConstraint('id', name=op.f('pk_oauth_accounts'))
    )


def downgrade() -> None:
    """Downgrade schema."""
    op.drop_table('oauth_accounts')
    op.drop_table('profiles')
    op.drop_table('roles')
    op.drop_table('oauth_providers')
