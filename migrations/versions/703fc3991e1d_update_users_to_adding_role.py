"""update users to adding role

Revision ID: 703fc3991e1d
Revises: c7cc84d44c9a
Create Date: 2024-12-18 11:05:33.974240

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '703fc3991e1d'
down_revision = 'c7cc84d44c9a'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('token_blocklist',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('jti', sa.String(length=255), nullable=False),
    sa.Column('created_at', sa.DateTime(), server_default=sa.text('now()'), nullable=True),
    sa.PrimaryKeyConstraint('id')
    )
    with op.batch_alter_table('users', schema=None) as batch_op:
        batch_op.add_column(sa.Column('role', sa.String(length=55), nullable=False))

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('users', schema=None) as batch_op:
        batch_op.drop_column('role')

    op.drop_table('token_blocklist')
    # ### end Alembic commands ###
