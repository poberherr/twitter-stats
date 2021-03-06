"""empty message

Revision ID: 1251ef11791b
Revises: 1f4aa62844c9
Create Date: 2016-02-21 16:04:24.662291

"""

# revision identifiers, used by Alembic.
revision = '1251ef11791b'
down_revision = '1f4aa62844c9'

from alembic import op
import sqlalchemy as sa


def upgrade():
    ### commands auto generated by Alembic - please adjust! ###
    op.add_column('users', sa.Column('is_follower_fetched', sa.Boolean(), nullable=True))
    ### end Alembic commands ###


def downgrade():
    ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('users', 'is_follower_fetched')
    ### end Alembic commands ###
