"""add-league-and-tournament-to-rating-history

Revision ID: ab98e9beee64
Revises: 8051efae9c40
Create Date: 2024-06-23 22:00:24.878515

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'ab98e9beee64'
down_revision: Union[str, None] = '8051efae9c40'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('rating_history', sa.Column('league_id', sa.Integer(), nullable=True))
    op.add_column('rating_history', sa.Column('tournament_id', sa.Integer(), nullable=True))
    op.create_foreign_key(None, 'rating_history', 'leagues', ['league_id'], ['id'])
    op.create_foreign_key(None, 'rating_history', 'tournaments', ['tournament_id'], ['id'])
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_constraint(None, 'rating_history', type_='foreignkey')
    op.drop_constraint(None, 'rating_history', type_='foreignkey')
    op.drop_column('rating_history', 'tournament_id')
    op.drop_column('rating_history', 'league_id')
    # ### end Alembic commands ###
