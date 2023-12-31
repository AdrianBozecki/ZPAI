"""Change price to string

Revision ID: 122fbb741819
Revises: 9c42847fd8f4
Create Date: 2023-11-25 09:41:02.802838

"""
from typing import Sequence, Union

import sqlalchemy as sa

from alembic import op

# revision identifiers, used by Alembic.
revision: str = "122fbb741819"
down_revision: Union[str, None] = "9c42847fd8f4"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.alter_column(
        "meals", "price", existing_type=sa.INTEGER(), type_=sa.String(), existing_nullable=True
    )
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.alter_column(
        "meals", "price", existing_type=sa.String(), type_=sa.INTEGER(), existing_nullable=True
    )
    # ### end Alembic commands ###
