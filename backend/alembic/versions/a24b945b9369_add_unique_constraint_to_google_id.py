"""Add unique constraint to google id

Revision ID: a24b945b9369
Revises: d49da7398ef9
Create Date: 2026-09-27 17:41:37.031286

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'a24b945b9369'
down_revision: Union[str, Sequence[str], None] = 'd49da7398ef9'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    op.create_unique_constraint(
            'uq_users_google_id',
            'users',
            ['google_id']
        )


def downgrade() -> None:
    """Downgrade schema."""
    op.drop_constraint(
            'uq_users_google_id',
            'users',
            type_='unique'
        )
