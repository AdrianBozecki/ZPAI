"""initial 

Revision ID: 675b3c2aa2bc
Revises: 
Create Date: 2024-07-07 08:18:51.690255

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '675b3c2aa2bc'
down_revision: Union[str, None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('category',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('name', sa.String(), nullable=False),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('name')
    )
    op.execute(
        "INSERT INTO category (name) VALUES ('Breakfast'), ('Lunch'), ('Dinner'), ('Snack'), ('Dessert'), ('Supper'), ('Drink'), ('Others')")
    op.create_table('user_details',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('name', sa.String(), nullable=False),
    sa.Column('lastname', sa.String(), nullable=False),
    sa.Column('phone_number', sa.String(), nullable=False),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_user_details_id'), 'user_details', ['id'], unique=False)
    op.create_index(op.f('ix_user_details_lastname'), 'user_details', ['lastname'], unique=False)
    op.create_index(op.f('ix_user_details_name'), 'user_details', ['name'], unique=False)
    op.create_index(op.f('ix_user_details_phone_number'), 'user_details', ['phone_number'], unique=False)
    op.create_table('user',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('email', sa.String(), nullable=False),
    sa.Column('password', sa.String(), nullable=False),
    sa.Column('user_details_id', sa.Integer(), nullable=False),
    sa.ForeignKeyConstraint(['user_details_id'], ['user_details.id'], ),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('email')
    )
    op.create_table('meal',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('name', sa.String(), nullable=False),
    sa.Column('description', sa.String(), nullable=False),
    sa.Column('user_id', sa.Integer(), nullable=False),
    sa.Column('preparation', sa.String(), nullable=False),
    sa.ForeignKeyConstraint(['user_id'], ['user.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('comment',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('content', sa.String(), nullable=False),
    sa.Column('user_id', sa.Integer(), nullable=False),
    sa.Column('meal_id', sa.Integer(), nullable=False),
    sa.ForeignKeyConstraint(['meal_id'], ['meal.id'], ),
    sa.ForeignKeyConstraint(['user_id'], ['user.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('like',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('user_id', sa.Integer(), nullable=False),
    sa.Column('meal_id', sa.Integer(), nullable=False),
    sa.ForeignKeyConstraint(['meal_id'], ['meal.id'], ),
    sa.ForeignKeyConstraint(['user_id'], ['user.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('meal_category_association',
    sa.Column('meal_id', sa.Integer(), nullable=True),
    sa.Column('category_id', sa.Integer(), nullable=True),
    sa.ForeignKeyConstraint(['category_id'], ['category.id'], ),
    sa.ForeignKeyConstraint(['meal_id'], ['meal.id'], )
    )
    op.create_table('product',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('name', sa.String(), nullable=False),
    sa.Column('unit_of_measure', sa.Enum('GRAM', 'KILOGRAM', 'MILLILITER', 'LITER', 'PIECE', 'OUNCE', 'POUND', 'PINT', 'QUART', 'GALLON', 'TEASPOON', 'TABLESPOON', 'CUP', name='unitofmeasureenum'), nullable=False),
    sa.Column('value', sa.Float(), nullable=False),
    sa.Column('meal_id', sa.Integer(), nullable=False),
    sa.ForeignKeyConstraint(['meal_id'], ['meal.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('product')
    op.drop_table('meal_category_association')
    op.drop_table('like')
    op.drop_table('comment')
    op.drop_table('meal')
    op.drop_table('user')
    op.drop_index(op.f('ix_user_details_phone_number'), table_name='user_details')
    op.drop_index(op.f('ix_user_details_name'), table_name='user_details')
    op.drop_index(op.f('ix_user_details_lastname'), table_name='user_details')
    op.drop_index(op.f('ix_user_details_id'), table_name='user_details')
    op.drop_table('user_details')
    op.execute("DELETE FROM category WHERE name IN ('Breakfast', 'Lunch', 'Dinner', 'Snack', 'Dessert', 'Supper', 'Drink', 'Others')")
    op.drop_table('category')
    # ### end Alembic commands ###
