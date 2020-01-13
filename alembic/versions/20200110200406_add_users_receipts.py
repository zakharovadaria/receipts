"""add_users_receipts

Revision ID: 20200110200406
Revises: 20200107180428
Create Date: 2020-01-10 20:04:07.538446

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '20200110200406'
down_revision = '20200107180428'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('users_receipts',
    sa.Column('user_id', sa.Integer(), nullable=False),
    sa.Column('receipt_id', sa.Integer(), nullable=False),
    sa.ForeignKeyConstraint(['receipt_id'], ['receipts.id'], ),
    sa.ForeignKeyConstraint(['user_id'], ['users.id'], ),
    sa.PrimaryKeyConstraint('user_id', 'receipt_id')
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('users_receipts')
    # ### end Alembic commands ###