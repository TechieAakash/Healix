"""Persist dataset-ranking output and question-to-evidence links.

Revision ID: 8b12e6d4a310
Revises: 7a1e3d2c9b40
Create Date: 2026-10-22
"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


revision: str = "8b12e6d4a310"
down_revision: Union[str, Sequence[str], None] = "7a1e3d2c9b40"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def _columns(table: str) -> set[str]:
    inspector = sa.inspect(op.get_bind())
    return {column["name"] for column in inspector.get_columns(table)} if table in inspector.get_table_names() else set()


def upgrade() -> None:
    inspector = sa.inspect(op.get_bind())
    tables = set(inspector.get_table_names())
    if "reports" in tables and "condition_ranking" not in _columns("reports"):
        op.add_column("reports", sa.Column("condition_ranking", sa.JSON(), nullable=False, server_default="[]"))
    if "follow_up_questions" in tables and "evidence_code" not in _columns("follow_up_questions"):
        op.add_column("follow_up_questions", sa.Column("evidence_code", sa.String(length=50), nullable=True))


def downgrade() -> None:
    if "evidence_code" in _columns("follow_up_questions"):
        op.drop_column("follow_up_questions", "evidence_code")
    if "condition_ranking" in _columns("reports"):
        op.drop_column("reports", "condition_ranking")
