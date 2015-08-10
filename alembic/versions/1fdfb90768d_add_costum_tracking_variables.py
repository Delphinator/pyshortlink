"""add costum_tracking_variables

Revision ID: 1fdfb90768d
Revises: 1e22c602120
Create Date: 2015-08-11 00:58:20.155455

"""

# revision identifiers, used by Alembic.
revision = '1fdfb90768d'
down_revision = '1e22c602120'
branch_labels = None
depends_on = None

import sqlalchemy as sa
from alembic import op
from sqlalchemy.dialects import postgresql


def upgrade():
    op.add_column(
        'link',
        sa.Column(
            'costum_tracking_variables',
            postgresql.HSTORE(),
            server_default=sa.text("''::hstore"),
            nullable=False
        )
    )


def downgrade():
    op.drop_column('link', 'costum_tracking_variables')
