"""Removed Unique flag on description fields

Revision ID: f53c5448e443
Revises: 832465548595
Create Date: 2023-03-13 18:03:09.668027

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'f53c5448e443'
down_revision = '832465548595'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('permissions', schema=None) as batch_op:
        batch_op.alter_column('description',
               existing_type=sa.VARCHAR(length=100),
               type_=sa.String(length=300),
               nullable=False)

    with op.batch_alter_table('roles', schema=None) as batch_op:
        batch_op.alter_column('description',
               existing_type=sa.VARCHAR(length=300),
               nullable=False)

    with op.batch_alter_table('users', schema=None) as batch_op:
        batch_op.alter_column('username',
               existing_type=sa.VARCHAR(length=50),
               nullable=False)

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('users', schema=None) as batch_op:
        batch_op.alter_column('username',
               existing_type=sa.VARCHAR(length=50),
               nullable=True)

    with op.batch_alter_table('roles', schema=None) as batch_op:
        batch_op.alter_column('description',
               existing_type=sa.VARCHAR(length=300),
               nullable=True)

    with op.batch_alter_table('permissions', schema=None) as batch_op:
        batch_op.alter_column('description',
               existing_type=sa.String(length=300),
               type_=sa.VARCHAR(length=100),
               nullable=True)

    # ### end Alembic commands ###