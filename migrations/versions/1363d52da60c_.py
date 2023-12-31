"""empty message

Revision ID: 1363d52da60c
Revises: 
Create Date: 2023-11-14 13:30:31.962588

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '1363d52da60c'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('items', schema=None) as batch_op:
        batch_op.add_column(sa.Column('description', sa.String(), nullable=True))

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('items', schema=None) as batch_op:
        batch_op.drop_column('description')

    # ### end Alembic commands ###
