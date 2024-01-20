"""update meal

Revision ID: fb0fc7f85663
Revises: 84791afd086a
Create Date: 2024-01-20 11:39:45.624676

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'fb0fc7f85663'
down_revision: Union[str, None] = '84791afd086a'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('meal', sa.Column('preparation', sa.String(), nullable=False))
    op.create_unique_constraint(None, 'product', ['name'])
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_constraint(None, 'product', type_='unique')
    op.drop_column('meal', 'preparation')
    # ### end Alembic commands ###