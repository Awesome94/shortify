"""empty message

Revision ID: b3b517a5e022
Revises: 
Create Date: 2017-02-27 13:39:38.054585

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'b3b517a5e022'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('user',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('username', sa.String(length=100), nullable=True),
    sa.Column('email', sa.String(length=100), nullable=True),
    sa.Column('password', sa.String(length=90), nullable=True),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('urlsSchema',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('title', sa.String(length=255), nullable=True),
    sa.Column('long_url', sa.String(length=255), nullable=True),
    sa.Column('short_url', sa.String(length=100), nullable=True),
    sa.Column('clicks', sa.Integer(), nullable=True),
    sa.Column('active', sa.Boolean(), nullable=False),
    sa.Column('author_id', sa.Integer(), nullable=True),
    sa.Column('timestamp', sa.DateTime(), nullable=True),
    sa.ForeignKeyConstraint(['author_id'], ['user.id'], ),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('short_url')
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('urlsSchema')
    op.drop_table('user')
    # ### end Alembic commands ###