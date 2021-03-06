"""empty message

Revision ID: 33c2e51098d7
Revises: None
Create Date: 2016-02-19 15:35:57.242751

"""

# revision identifiers, used by Alembic.
revision = '33c2e51098d7'
down_revision = None

from alembic import op
import sqlalchemy as sa


def upgrade():
    ### commands auto generated by Alembic - please adjust! ###
    op.create_table('users',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('name', sa.String(length=250), nullable=True),
    sa.Column('screen_name', sa.String(length=250), nullable=True),
    sa.Column('location', sa.String(length=250), nullable=True),
    sa.Column('description', sa.String(length=250), nullable=True),
    sa.Column('url', sa.String(length=250), nullable=True),
    sa.Column('followers_count', sa.Integer(), nullable=True),
    sa.Column('friends_count', sa.Integer(), nullable=True),
    sa.Column('created_at', sa.TIMESTAMP(), nullable=True),
    sa.Column('favourites_count', sa.Integer(), nullable=True),
    sa.Column('time_zone', sa.String(length=250), nullable=True),
    sa.Column('statuses_count', sa.Integer(), nullable=True),
    sa.Column('modified_at', sa.TIMESTAMP(), server_default=sa.text('CURRENT_TIMESTAMP'), nullable=False),
    sa.PrimaryKeyConstraint('id')
    )
    ### end Alembic commands ###


def downgrade():
    ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('users')
    ### end Alembic commands ###
