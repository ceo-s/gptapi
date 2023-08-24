"""

Revision ID: 142ac8510688
Revises: 
Create Date: 2023-08-24 16:44:57.967183

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql
from pgvector.sqlalchemy import Vector

# revision identifiers, used by Alembic.
revision: str = '142ac8510688'
down_revision: Union[str, None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None

# autopep8: off
def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('user',
    sa.Column('id', sa.BigInteger(), nullable=False),
    sa.Column('username', sa.String(length=36), nullable=False),
    sa.Column('first_name', sa.String(length=32), nullable=False),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('collection',
    sa.Column('dir_id', sa.String(), nullable=False),
    sa.Column('user_fk', sa.BigInteger(), nullable=False),
    sa.Column('id', sa.Integer(), autoincrement=True, nullable=False),
    sa.ForeignKeyConstraint(['user_fk'], ['user.id'], ondelete='CASCADE'),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('user_settings',
    sa.Column('model_temperature', sa.Float(), nullable=False),
    sa.Column('prompt', sa.String(), nullable=False),
    sa.Column('history', postgresql.JSONB(astext_type=sa.Text()), nullable=True),
    sa.Column('history_size', sa.Integer(), nullable=False),
    sa.Column('user_fk', sa.BigInteger(), nullable=False),
    sa.Column('id', sa.Integer(), autoincrement=True, nullable=False),
    sa.ForeignKeyConstraint(['user_fk'], ['user.id'], ondelete='CASCADE'),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('drive_file',
    sa.Column('file_id', sa.String(), nullable=False),
    sa.Column('content', sa.String(), nullable=False),
    sa.Column('collection_fk', sa.Integer(), nullable=False),
    sa.ForeignKeyConstraint(['collection_fk'], ['collection.id'], ),
    sa.PrimaryKeyConstraint('file_id')
    )
    op.create_table('document',
    sa.Column('text', sa.String(), nullable=False),
    sa.Column('embedding', Vector(dim=1536), nullable=True),
    sa.Column('drive_file_fk', sa.String(), nullable=False),
    sa.Column('id', sa.Integer(), autoincrement=True, nullable=False),
    sa.ForeignKeyConstraint(['drive_file_fk'], ['drive_file.file_id'], ondelete='CASCADE'),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('document_metadata',
    sa.Column('name', sa.String(), nullable=False),
    sa.Column('description', sa.String(), nullable=True),
    sa.Column('token_cost', sa.Integer(), nullable=True),
    sa.Column('drive_file_fk', sa.String(), nullable=False),
    sa.Column('id', sa.Integer(), autoincrement=True, nullable=False),
    sa.ForeignKeyConstraint(['drive_file_fk'], ['drive_file.file_id'], ondelete='CASCADE'),
    sa.PrimaryKeyConstraint('id')
    )
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('document_metadata')
    op.drop_table('document')
    op.drop_table('drive_file')
    op.drop_table('user_settings')
    op.drop_table('collection')
    op.drop_table('user')
    # ### end Alembic commands ###