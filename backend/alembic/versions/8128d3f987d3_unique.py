"""unique

Revision ID: 8128d3f987d3
Revises: d715edd90ccf
Create Date: 2024-07-07 09:46:43.879103

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '8128d3f987d3'
down_revision: Union[str, None] = 'd715edd90ccf'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_unique_constraint('_user_meal_uc', 'like', ['user_id', 'meal_id'])
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_constraint('_user_meal_uc', 'like', type_='unique')
    # ### end Alembic commands ###