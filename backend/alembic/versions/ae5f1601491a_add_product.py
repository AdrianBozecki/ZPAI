"""add product

Revision ID: ae5f1601491a
Revises: 17a8da7bd990
Create Date: 2024-01-20 10:54:37.203366

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'ae5f1601491a'
down_revision: Union[str, None] = '17a8da7bd990'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('product',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('name', sa.String(), nullable=False),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('meal_product_association',
    sa.Column('meal_id', sa.Integer(), nullable=True),
    sa.Column('product_id', sa.Integer(), nullable=True),
    sa.ForeignKeyConstraint(['meal_id'], ['meal.id'], ),
    sa.ForeignKeyConstraint(['product_id'], ['product.id'], )
    )
    op.create_foreign_key(None, 'like', 'user', ['user_id'], ['id'])
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_constraint(None, 'like', type_='foreignkey')
    op.drop_table('meal_product_association')
    op.drop_table('product')
    # ### end Alembic commands ###