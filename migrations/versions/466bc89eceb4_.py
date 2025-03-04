"""empty message

Revision ID: 466bc89eceb4
Revises: 0ea90cb98558
Create Date: 2023-10-30 13:35:09.796296

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import mysql

# revision identifiers, used by Alembic.
revision = '466bc89eceb4'
down_revision = '0ea90cb98558'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('restaurant', schema=None) as batch_op:
        batch_op.add_column(sa.Column('address_city', sa.String(length=120), nullable=True))
        batch_op.add_column(sa.Column('address_housenumber', sa.String(length=120), nullable=True))
        batch_op.add_column(sa.Column('address_postcode', sa.String(length=120), nullable=True))
        batch_op.add_column(sa.Column('address_state', sa.String(length=120), nullable=True))
        batch_op.add_column(sa.Column('address_street', sa.String(length=120), nullable=True))
        batch_op.add_column(sa.Column('phone', sa.String(length=120), nullable=True))
        batch_op.add_column(sa.Column('website', sa.String(length=120), nullable=True))
        batch_op.add_column(sa.Column('cuisine', sa.String(length=120), nullable=True))
        batch_op.add_column(sa.Column('delivery', sa.Boolean(), nullable=True))
        batch_op.add_column(sa.Column('microbrewery', sa.Boolean(), nullable=True))
        batch_op.add_column(sa.Column('opening_hours', sa.String(length=120), nullable=True))
        batch_op.add_column(sa.Column('outdoor_seating', sa.Boolean(), nullable=True))
        batch_op.add_column(sa.Column('bar', sa.Boolean(), nullable=True))
        batch_op.add_column(sa.Column('brewery', sa.Boolean(), nullable=True))
        batch_op.add_column(sa.Column('takeaway', sa.Boolean(), nullable=True))
        batch_op.drop_index('ix_restaurant_address')
        batch_op.create_index(batch_op.f('ix_restaurant_address_city'), ['address_city'], unique=False)
        batch_op.create_index(batch_op.f('ix_restaurant_address_housenumber'), ['address_housenumber'], unique=False)
        batch_op.create_index(batch_op.f('ix_restaurant_address_postcode'), ['address_postcode'], unique=False)
        batch_op.create_index(batch_op.f('ix_restaurant_address_state'), ['address_state'], unique=False)
        batch_op.create_index(batch_op.f('ix_restaurant_address_street'), ['address_street'], unique=False)
        batch_op.create_index(batch_op.f('ix_restaurant_bar'), ['bar'], unique=False)
        batch_op.create_index(batch_op.f('ix_restaurant_brewery'), ['brewery'], unique=False)
        batch_op.create_index(batch_op.f('ix_restaurant_cuisine'), ['cuisine'], unique=False)
        batch_op.create_index(batch_op.f('ix_restaurant_delivery'), ['delivery'], unique=False)
        batch_op.create_index(batch_op.f('ix_restaurant_microbrewery'), ['microbrewery'], unique=False)
        batch_op.create_index(batch_op.f('ix_restaurant_opening_hours'), ['opening_hours'], unique=False)
        batch_op.create_index(batch_op.f('ix_restaurant_outdoor_seating'), ['outdoor_seating'], unique=False)
        batch_op.create_index(batch_op.f('ix_restaurant_phone'), ['phone'], unique=False)
        batch_op.create_index(batch_op.f('ix_restaurant_takeaway'), ['takeaway'], unique=False)
        batch_op.create_index(batch_op.f('ix_restaurant_website'), ['website'], unique=False)
        batch_op.drop_column('address')
        batch_op.drop_column('rating')

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('restaurant', schema=None) as batch_op:
        batch_op.add_column(sa.Column('rating', mysql.VARCHAR(length=50), nullable=True))
        batch_op.add_column(sa.Column('address', mysql.VARCHAR(length=120), nullable=True))
        batch_op.drop_index(batch_op.f('ix_restaurant_website'))
        batch_op.drop_index(batch_op.f('ix_restaurant_takeaway'))
        batch_op.drop_index(batch_op.f('ix_restaurant_phone'))
        batch_op.drop_index(batch_op.f('ix_restaurant_outdoor_seating'))
        batch_op.drop_index(batch_op.f('ix_restaurant_opening_hours'))
        batch_op.drop_index(batch_op.f('ix_restaurant_microbrewery'))
        batch_op.drop_index(batch_op.f('ix_restaurant_delivery'))
        batch_op.drop_index(batch_op.f('ix_restaurant_cuisine'))
        batch_op.drop_index(batch_op.f('ix_restaurant_brewery'))
        batch_op.drop_index(batch_op.f('ix_restaurant_bar'))
        batch_op.drop_index(batch_op.f('ix_restaurant_address_street'))
        batch_op.drop_index(batch_op.f('ix_restaurant_address_state'))
        batch_op.drop_index(batch_op.f('ix_restaurant_address_postcode'))
        batch_op.drop_index(batch_op.f('ix_restaurant_address_housenumber'))
        batch_op.drop_index(batch_op.f('ix_restaurant_address_city'))
        batch_op.create_index('ix_restaurant_address', ['address'], unique=False)
        batch_op.drop_column('takeaway')
        batch_op.drop_column('brewery')
        batch_op.drop_column('bar')
        batch_op.drop_column('outdoor_seating')
        batch_op.drop_column('opening_hours')
        batch_op.drop_column('microbrewery')
        batch_op.drop_column('delivery')
        batch_op.drop_column('cuisine')
        batch_op.drop_column('website')
        batch_op.drop_column('phone')
        batch_op.drop_column('address_street')
        batch_op.drop_column('address_state')
        batch_op.drop_column('address_postcode')
        batch_op.drop_column('address_housenumber')
        batch_op.drop_column('address_city')

    # ### end Alembic commands ###
