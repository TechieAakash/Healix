"""Persist rule explanations and follow-up rationale.

Revision ID: 7a1e3d2c9b40
Revises: af73c9aba7e1
Create Date: 2026-10-22
"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


revision: str = "7a1e3d2c9b40"
down_revision: Union[str, Sequence[str], None] = "af73c9aba7e1"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    inspector = sa.inspect(op.get_bind())
    tables = set(inspector.get_table_names())
    if "reports" in tables and "reasoning_trace" not in {c["name"] for c in inspector.get_columns("reports")}:
        op.add_column(
            "reports",
            sa.Column("reasoning_trace", sa.JSON(), nullable=False, server_default="[]"),
        )
    if "follow_up_questions" in tables and "reasoning" not in {c["name"] for c in inspector.get_columns("follow_up_questions")}:
        op.add_column("follow_up_questions", sa.Column("reasoning", sa.Text(), nullable=True))


def downgrade() -> None:
    inspector = sa.inspect(op.get_bind())
    tables = set(inspector.get_table_names())
    if "follow_up_questions" in tables and "reasoning" in {c["name"] for c in inspector.get_columns("follow_up_questions")}:
        op.drop_column("follow_up_questions", "reasoning")
    if "reports" in tables and "reasoning_trace" in {c["name"] for c in inspector.get_columns("reports")}:
        op.drop_column("reports", "reasoning_trace")
