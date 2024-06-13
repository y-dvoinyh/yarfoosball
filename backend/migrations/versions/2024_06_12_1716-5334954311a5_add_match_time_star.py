"""add-match-time_star

Revision ID: 5334954311a5
Revises: f0a97092bb5f
Create Date: 2024-06-12 17:16:23.959554

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '5334954311a5'
down_revision: Union[str, None] = 'f0a97092bb5f'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('matches', sa.Column('time_start', sa.DateTime(), nullable=True))
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('matches', 'time_start')
    # ### end Alembic commands ###