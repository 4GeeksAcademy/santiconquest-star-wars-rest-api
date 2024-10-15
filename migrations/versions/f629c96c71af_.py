"""empty message

Revision ID: f629c96c71af
Revises: dcb35a18082e
Create Date: 2024-10-14 20:40:40.041532

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'f629c96c71af'
down_revision = 'dcb35a18082e'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('planetas',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('name', sa.String(length=250), nullable=True),
    sa.Column('population', sa.String(length=250), nullable=True),
    sa.Column('terrain', sa.String(length=250), nullable=True),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('user_fav',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('user_id', sa.Integer(), nullable=True),
    sa.Column('personaje_id', sa.Integer(), nullable=True),
    sa.Column('planetas_id', sa.Integer(), nullable=True),
    sa.ForeignKeyConstraint(['personaje_id'], ['personajes.id'], ),
    sa.ForeignKeyConstraint(['planetas_id'], ['planetas.id'], ),
    sa.ForeignKeyConstraint(['user_id'], ['user.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('user_fav')
    op.drop_table('planetas')
    # ### end Alembic commands ###