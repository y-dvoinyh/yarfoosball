"""add place column

Revision ID: 29360402caee
Revises: ac1f672f56dd
Create Date: 2024-12-19 13:00:59.714589

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '29360402caee'
down_revision: Union[str, None] = 'ac1f672f56dd'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('rating_history', sa.Column('place', sa.Integer(), nullable=True))
    op.drop_column('rating_history', 'is_winner')
    op.drop_column('rating_history', 'is_draw')
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('rating_history', sa.Column('is_draw', sa.BOOLEAN(), autoincrement=False, nullable=True))
    op.add_column('rating_history', sa.Column('is_winner', sa.BOOLEAN(), autoincrement=False, nullable=True))
    op.drop_column('rating_history', 'place')
    # ### end Alembic commands ###