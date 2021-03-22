"""empty message

Revision ID: 81f7e2b8c618
Revises: 
Create Date: 2021-03-22 09:31:13.639885

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '81f7e2b8c618'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('property_info',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('title', sa.String(length=50), nullable=False),
    sa.Column('num_bedrooms', sa.Integer(), nullable=False),
    sa.Column('num_bathrooms', sa.Integer(), nullable=False),
    sa.Column('location', sa.String(length=50), nullable=False),
    sa.Column('price', sa.Numeric(precision=15, scale=2), nullable=False),
    sa.Column('type_', sa.String(length=50), nullable=False),
    sa.Column('description', sa.String(length=250), nullable=False),
    sa.Column('upload', sa.String(length=50), nullable=False),
    sa.Column('date_created', sa.Date(), nullable=False),
    sa.PrimaryKeyConstraint('id')
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('property_info')
    # ### end Alembic commands ###
