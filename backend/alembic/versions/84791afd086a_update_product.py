"""update_product

Revision ID: 84791afd086a
Revises: 485062be6f7b
Create Date: 2024-01-20 11:31:23.301438

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '84791afd086a'
down_revision: Union[str, None] = '485062be6f7b'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    unitofmeasureenum = sa.Enum('GRAM', 'MILLILITER', 'CENTIMETER', 'PIECE', name='unitofmeasureenum')
    unitofmeasureenum.create(op.get_bind(), checkfirst=True)  # Tworzy enum, jeśli jeszcze nie istnieje
    op.add_column('product', sa.Column('unit_of_measure', unitofmeasureenum, nullable=False))

def downgrade() -> None:
    op.drop_column('product', 'unit_of_measure')
    unitofmeasureenum = sa.Enum(name='unitofmeasureenum')
    unitofmeasureenum.drop(op.get_bind(), checkfirst=True)
