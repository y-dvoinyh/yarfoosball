"""extend rank enum

Revision ID: f28f1ac65b2b
Revises: 282ad7eaa918
Create Date: 2026-03-04 11:02:34.735533

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'f28f1ac65b2b'
down_revision: Union[str, None] = '282ad7eaa918'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.execute("ALTER TYPE rank_enum ADD VALUE IF NOT EXISTS 'low_minus'")
    op.execute("ALTER TYPE rank_enum ADD VALUE IF NOT EXISTS 'low'")
    op.execute("ALTER TYPE rank_enum ADD VALUE IF NOT EXISTS 'low_plus'")
    op.execute("ALTER TYPE rank_enum ADD VALUE IF NOT EXISTS 'mid_minus'")
    op.execute("ALTER TYPE rank_enum ADD VALUE IF NOT EXISTS 'mid'")
    op.execute("ALTER TYPE rank_enum ADD VALUE IF NOT EXISTS 'mid_plus'")
    op.execute("ALTER TYPE rank_enum ADD VALUE IF NOT EXISTS 'high_minus'")
    op.execute("ALTER TYPE rank_enum ADD VALUE IF NOT EXISTS 'high'")
    op.execute("ALTER TYPE rank_enum ADD VALUE IF NOT EXISTS 'high_plus'")
    op.execute("ALTER TYPE rank_enum ADD VALUE IF NOT EXISTS 'new_pro'")
    op.execute("ALTER TYPE rank_enum ADD VALUE IF NOT EXISTS 'pro_plus'")


def downgrade() -> None:
    pass
