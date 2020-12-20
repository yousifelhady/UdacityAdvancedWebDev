"""empty message

Revision ID: 18dc74c84488
Revises: 60c31b9ed078
Create Date: 2020-12-20 22:21:10.099039

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '18dc74c84488'
down_revision = '60c31b9ed078'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.alter_column('todos', 'list_id',
               existing_type=sa.INTEGER(),
               nullable=False)
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.alter_column('todos', 'list_id',
               existing_type=sa.INTEGER(),
               nullable=True)
    # ### end Alembic commands ###
