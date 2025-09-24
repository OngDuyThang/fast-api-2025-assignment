"""generate company table

Revision ID: af763c0ca2d1
Revises:
Create Date: 2025-09-23 21:27:49.808820

"""

from typing import Sequence, Union

import sqlalchemy as sa
from alembic import op
from common.enums import CompanyMode

# revision identifiers, used by Alembic.
revision: str = "af763c0ca2d1"
down_revision: Union[str, Sequence[str], None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.create_table(
        "companies",
        sa.Column("id", sa.UUID, primary_key=True, nullable=False),
        sa.Column("name", sa.String(length=100), nullable=False),
        sa.Column("description", sa.String, nullable=True),
        sa.Column(
            "mode", sa.Enum(CompanyMode), nullable=False, default=CompanyMode.OUTSOURCE
        ),
        sa.Column("rating", sa.Float, nullable=False, default=0),
        sa.Column("created_at", sa.DateTime),
        sa.Column("updated_at", sa.DateTime),
    )


def downgrade() -> None:
    op.drop_table("companies")
    op.execute("DROP TYPE companymode;")
