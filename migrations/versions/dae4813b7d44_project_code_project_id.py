"""project_code -> project_id

Revision ID: dae4813b7d44
Revises: 4b9e9f41d3ad
Create Date: 2024-10-16 23:03:55.191030

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'dae4813b7d44'
down_revision: Union[str, None] = '4b9e9f41d3ad'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('journals', sa.Column('project_id', sa.String(), nullable=True))
    op.drop_column('journals', 'project_code')
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('journals', sa.Column('project_code', sa.VARCHAR(), nullable=False))
    op.drop_column('journals', 'project_id')
    # ### end Alembic commands ###