"""Remove likes

Revision ID: 8e4f953d3fbc
Revises: fb0fc7f85663
Create Date: 2024-01-28 17:19:58.059791

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
revision: str = '8e4f953d3fbc'
down_revision: Union[str, None] = 'fb0fc7f85663'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('like')
    op.drop_column('meal', 'likes_count')
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('meal', sa.Column('likes_count', sa.INTEGER(), autoincrement=False, nullable=False))
    op.create_table('like',
    sa.Column('id', sa.INTEGER(), autoincrement=True, nullable=False),
    sa.Column('user_id', sa.INTEGER(), autoincrement=False, nullable=False),
    sa.Column('meal_id', sa.INTEGER(), autoincrement=False, nullable=False),
    sa.Column('value', postgresql.ENUM('LIKE', 'DISLIKE', name='likedislikeenum'), autoincrement=False, nullable=False),
    sa.ForeignKeyConstraint(['meal_id'], ['meal.id'], name='like_meal_id_fkey'),
    sa.ForeignKeyConstraint(['user_id'], ['user.id'], name='like_user_id_fkey'),
    sa.PrimaryKeyConstraint('id', name='like_pkey')
    )
    # ### end Alembic commands ###