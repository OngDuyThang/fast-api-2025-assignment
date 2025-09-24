"""generate user table

Revision ID: d9797ef0d160
Revises: af763c0ca2d1
Create Date: 2025-09-23 21:29:33.301721

"""

from datetime import datetime, timezone
from typing import Sequence, Union
from uuid import uuid4

import sqlalchemy as sa
from alembic import op
from services.auth import create_hashed_password
from settings import ADMIN_DEFAULT_PASSWORD

# revision identifiers, used by Alembic.
revision: str = "d9797ef0d160"
down_revision: Union[str, Sequence[str], None] = "af763c0ca2d1"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # User Table
    user_table = op.create_table(
        "users",
        sa.Column("id", sa.UUID, primary_key=True, nullable=False),
        sa.Column(
            "email", sa.String(length=100), unique=True, index=True, nullable=True
        ),
        sa.Column("username", sa.String(length=100), unique=True, index=True),
        sa.Column("first_name", sa.String(length=100)),
        sa.Column("last_name", sa.String(length=100)),
        sa.Column("password", sa.String),
        sa.Column("is_active", sa.Boolean, default=True),
        sa.Column("is_admin", sa.Boolean, default=False),
        sa.Column("created_at", sa.DateTime),
        sa.Column("updated_at", sa.DateTime),
    )

    # Update User Table
    op.add_column("users", sa.Column("company_id", sa.UUID, nullable=True))
    op.create_foreign_key(
        "fk_user_company", "users", "companies", ["company_id"], ["id"]
    )

    # Data seed for first user
    op.bulk_insert(
        user_table,
        [
            {
                "id": uuid4(),
                "email": "admin@sample.com",
                "username": "admin",
                "password": create_hashed_password(ADMIN_DEFAULT_PASSWORD),
                "first_name": "Admin",
                "last_name": "Admin",
                "is_active": True,
                "is_admin": True,
                "created_at": datetime.now(timezone.utc),
                "updated_at": datetime.now(timezone.utc),
            }
        ],
    )


def downgrade() -> None:
    # Rollback foreign key
    op.drop_column("users", "company_id")
    op.drop_table("users")
