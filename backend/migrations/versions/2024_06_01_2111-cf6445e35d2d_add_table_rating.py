"""add-table-rating

Revision ID: cf6445e35d2d
Revises: 6904bc72f053
Create Date: 2024-06-01 21:11:23.079901

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
revision: str = 'cf6445e35d2d'
down_revision: Union[str, None] = '6904bc72f053'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    sa.Enum('PLAYER', 'LEAGUE', 'TOURNAMENT', name='rating_type_enum').create(op.get_bind())
    op.create_table('ratings',
    sa.Column('type', postgresql.ENUM('PLAYER', 'LEAGUE', 'TOURNAMENT', name='rating_type_enum', create_type=False), nullable=False),
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('created_at', sa.DateTime(), nullable=False),
    sa.Column('updated_at', sa.TIMESTAMP(timezone=True), nullable=False),
    sa.PrimaryKeyConstraint('id')
    )
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('ratings')
    sa.Enum('PLAYER', 'LEAGUE', 'TOURNAMENT', name='rating_type_enum').drop(op.get_bind())
    # ### end Alembic commands ###