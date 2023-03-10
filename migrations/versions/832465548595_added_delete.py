"""Added Delete

Revision ID: 832465548595
Revises: 2e51cb3ce377
Create Date: 2023-03-12 18:58:17.197598

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '832465548595'
down_revision = '2e51cb3ce377'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('blacklist_tokens', schema=None) as batch_op:
        batch_op.add_column(sa.Column('deleted', sa.Boolean(), nullable=True))

    with op.batch_alter_table('permissions', schema=None) as batch_op:
        batch_op.add_column(sa.Column('deleted', sa.Boolean(), nullable=True))

    with op.batch_alter_table('role_permissions', schema=None) as batch_op:
        batch_op.add_column(sa.Column('deleted', sa.Boolean(), nullable=True))

    with op.batch_alter_table('roles', schema=None) as batch_op:
        batch_op.add_column(sa.Column('deleted', sa.Boolean(), nullable=True))

    with op.batch_alter_table('user_roles', schema=None) as batch_op:
        batch_op.add_column(sa.Column('deleted', sa.Boolean(), nullable=True))

    with op.batch_alter_table('users', schema=None) as batch_op:
        batch_op.add_column(sa.Column('deleted', sa.Boolean(), nullable=True))

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('users', schema=None) as batch_op:
        batch_op.drop_column('deleted')

    with op.batch_alter_table('user_roles', schema=None) as batch_op:
        batch_op.drop_column('deleted')

    with op.batch_alter_table('roles', schema=None) as batch_op:
        batch_op.drop_column('deleted')

    with op.batch_alter_table('role_permissions', schema=None) as batch_op:
        batch_op.drop_column('deleted')

    with op.batch_alter_table('permissions', schema=None) as batch_op:
        batch_op.drop_column('deleted')

    with op.batch_alter_table('blacklist_tokens', schema=None) as batch_op:
        batch_op.drop_column('deleted')

    # ### end Alembic commands ###
