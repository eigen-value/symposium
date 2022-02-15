"""participant approval flag

Revision ID: e2fa0407a065
Revises: 8e7a87f3478b
Create Date: 2022-02-14 18:02:01.824248

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'e2fa0407a065'
down_revision = '8e7a87f3478b'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('participant', schema=None) as batch_op:
        batch_op.add_column(sa.Column('approved_subscription', sa.Boolean(), nullable=True))

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('participant', schema=None) as batch_op:
        batch_op.drop_column('approved_subscription')

    # ### end Alembic commands ###