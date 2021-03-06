"""create_ingredients

Revision ID: 20191113142928
Revises: 
Create Date: 2019-11-13 14:29:29.434582

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '20191113142928'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('ingredients',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('name', sa.String(), nullable=True),
    sa.Column('calories', sa.Float(), nullable=True),
    sa.PrimaryKeyConstraint('id')
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('ingredients')
    # ### end Alembic commands ###
