"""rounds table - add column

Revision ID: 2e26f77645d1
Revises: 40520639d18e
Create Date: 2024-02-06 05:45:11.010249

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '2e26f77645d1'
down_revision = '40520639d18e'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('round', schema=None) as batch_op:
        batch_op.add_column(sa.Column('difficulty', sa.String(length=100), nullable=False))

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('round', schema=None) as batch_op:
        batch_op.drop_column('difficulty')

    # ### end Alembic commands ###
