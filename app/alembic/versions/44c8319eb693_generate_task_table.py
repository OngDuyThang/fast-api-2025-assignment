"""generate task table

Revision ID: 44c8319eb693
Revises: d9797ef0d160
Create Date: 2025-09-23 21:36:48.871337

"""

from typing import Sequence, Union

import sqlalchemy as sa
from alembic import op
from common.enums import TaskPriority, TaskStatus

# revision identifiers, used by Alembic.
revision: str = "44c8319eb693"
down_revision: Union[str, Sequence[str], None] = "d9797ef0d160"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.create_table(
        "tasks",
        sa.Column("id", sa.UUID, primary_key=True, nullable=False),
        sa.Column("summary", sa.String(length=500), nullable=True),
        sa.Column("description", sa.String(length=500), nullable=True),
        sa.Column(
            "status", sa.Enum(TaskStatus), nullable=False, default=TaskStatus.BACKLOG
        ),
        sa.Column(
            "priority", sa.Enum(TaskPriority), nullable=False, default=TaskPriority.LOW
        ),
        sa.Column("created_at", sa.DateTime),
        sa.Column("updated_at", sa.DateTime),
    )

    op.add_column("tasks", sa.Column("owner_id", sa.UUID, nullable=True))
    op.create_foreign_key("fk_task_owner", "tasks", "users", ["owner_id"], ["id"])


def downgrade() -> None:
    op.drop_column("tasks", "owner_id")
    op.drop_table("tasks")
    op.execute("DROP TYPE taskstatus;")
    op.execute("DROP TYPE taskpriority;")
