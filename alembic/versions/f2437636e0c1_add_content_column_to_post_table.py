"""add content column to post table

Revision ID: f2437636e0c1
Revises: d47938c11c2f
Create Date: 2024-05-23 19:33:24.134941

"""

from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = "f2437636e0c1"
down_revision: Union[str, None] = "d47938c11c2f"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.add_column("posts", sa.Column("content", sa.String(), nullable=False))
    pass


def downgrade() -> None:
    op.drop_column("posts", "content")
    pass
