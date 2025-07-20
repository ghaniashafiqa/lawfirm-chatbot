"""recreate missing

Revision ID: ec7e5b56143d
Revises: 
Create Date: 2025-07-20 20:37:19.613735
"""

from alembic import op
import sqlalchemy as sa

# revision identifiers, used by Alembic.
revision = 'ec7e5b56143d'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    op.create_table(
        'admins',
        sa.Column('id', sa.Integer(), primary_key=True),
        sa.Column('username', sa.String(length=50), nullable=False, unique=True),
        sa.Column('email', sa.String(length=100), nullable=False, unique=True),
        sa.Column('password_h', sa.Text(), nullable=False),
        sa.Column('role', sa.String(length=20), nullable=True, server_default='admin'),
        sa.Column('created_at', sa.DateTime(), server_default=sa.func.now())
    )

    op.create_table(
        'sessions',
        sa.Column('id', sa.Integer(), primary_key=True),
        sa.Column('admin_id', sa.Integer(), sa.ForeignKey('admins.id'), nullable=False),
        sa.Column('ip', sa.String(length=50)),
        sa.Column('device', sa.String(length=100)),
        sa.Column('location', sa.String(length=100)),
        sa.Column('user_agent', sa.Text()),
        sa.Column('current', sa.Boolean(), server_default=sa.text('true')),
        sa.Column('last_active', sa.DateTime(), default=sa.func.now())
    )

    op.create_table(
        'chat_history',
        sa.Column('id', sa.Integer(), primary_key=True),
        sa.Column('session_id', sa.String(length=36), nullable=False),
        sa.Column('question', sa.Text(), nullable=False),
        sa.Column('answer', sa.Text(), nullable=False),
        sa.Column('created_at', sa.DateTime(), server_default=sa.func.now())
    )

    op.create_table(
        'faq',
        sa.Column('id', sa.Integer(), primary_key=True),
        sa.Column('question', sa.Text(), nullable=False),
        sa.Column('answer', sa.Text(), nullable=False),
        sa.Column('created_at', sa.DateTime(), server_default=sa.func.now())
    )

    op.create_table(
        'bot_greetings',
        sa.Column('id', sa.Integer(), primary_key=True),
        sa.Column('text', sa.String(length=255), nullable=False),
        sa.Column('created_at', sa.DateTime(), server_default=sa.func.now())
    )

    op.create_table(
        'settings',
        sa.Column('id', sa.Integer(), primary_key=True),
        sa.Column('key', sa.String(length=50), nullable=False, unique=True),
        sa.Column('value', sa.Text(), nullable=False),
        sa.Column('updated_at', sa.DateTime(), server_default=sa.func.now(), onupdate=sa.func.now())
    )

    op.create_table(
        'feedback',
        sa.Column('id', sa.Integer(), primary_key=True),
        sa.Column('chat_id', sa.Integer(), sa.ForeignKey('chat_history.id'), nullable=False),
        sa.Column('is_positive', sa.Boolean(), nullable=False),
        sa.Column('comment', sa.Text()),
        sa.Column('created_at', sa.DateTime(), server_default=sa.func.now())
    )


def downgrade():
    op.drop_table('feedback')
    op.drop_table('settings')
    op.drop_table('bot_greetings')
    op.drop_table('faq')
    op.drop_table('chat_history')
    op.drop_table('sessions')
    op.drop_table('admins')
