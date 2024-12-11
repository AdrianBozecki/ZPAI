"""add_image_url

Revision ID: 691b5261b175
Revises: 8128d3f987d3
Create Date: 2024-08-06 19:49:30.977945

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '691b5261b175'
down_revision: Union[str, None] = '8128d3f987d3'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('meal_product_association')
    op.add_column('meal', sa.Column('image_url', sa.String(), nullable=True))
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('meal', 'image_url')
    op.create_table('meal_product_association',
    sa.Column('meal_id', sa.INTEGER(), autoincrement=False, nullable=True),
    sa.Column('product_id', sa.INTEGER(), autoincrement=False, nullable=True),
    sa.ForeignKeyConstraint(['meal_id'], ['meal.id'], name='meal_product_association_meal_id_fkey'),
    sa.ForeignKeyConstraint(['product_id'], ['product.id'], name='meal_product_association_product_id_fkey')
    )
    # ### end Alembic commands ###