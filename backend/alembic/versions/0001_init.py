"""init

Revision ID: 0001_init
Revises:
Create Date: 2026-04-26
"""

from alembic import op
import sqlalchemy as sa

revision = '0001_init'
down_revision = None
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.create_table('restaurants', sa.Column('id', sa.Integer(), primary_key=True), sa.Column('name', sa.String(255), nullable=False), sa.Column('default_dialect', sa.String(50), nullable=False), sa.Column('active', sa.Boolean(), nullable=False))
    op.create_table('branches', sa.Column('id', sa.Integer(), primary_key=True), sa.Column('restaurant_id', sa.Integer(), sa.ForeignKey('restaurants.id'), nullable=False), sa.Column('name', sa.String(255), nullable=False), sa.Column('phone', sa.String(50), nullable=False), sa.Column('address', sa.Text(), nullable=False), sa.Column('timezone', sa.String(64), nullable=False))
    op.create_table('menu_categories', sa.Column('id', sa.Integer(), primary_key=True), sa.Column('restaurant_id', sa.Integer(), sa.ForeignKey('restaurants.id'), nullable=False), sa.Column('name_ar', sa.String(255), nullable=False))
    op.create_table('menu_items', sa.Column('id', sa.Integer(), primary_key=True), sa.Column('restaurant_id', sa.Integer(), sa.ForeignKey('restaurants.id'), nullable=False), sa.Column('category_id', sa.Integer(), sa.ForeignKey('menu_categories.id'), nullable=False), sa.Column('name_ar', sa.String(255), nullable=False), sa.Column('description_ar', sa.Text(), nullable=False), sa.Column('price', sa.Numeric(10, 2), nullable=False), sa.Column('is_available', sa.Boolean(), nullable=False))


def downgrade() -> None:
    op.drop_table('menu_items')
    op.drop_table('menu_categories')
    op.drop_table('branches')
    op.drop_table('restaurants')
