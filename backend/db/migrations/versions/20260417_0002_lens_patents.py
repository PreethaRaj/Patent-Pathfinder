"""add patent ingestion tables

Revision ID: 20260417_0002
Revises: 20260417_0001
Create Date: 2026-04-17 00:20:00
"""

from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

revision = "20260417_0002"
down_revision = "20260417_0001"
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.create_table(
        "patent_documents",
        sa.Column("id", postgresql.UUID(as_uuid=True), primary_key=True, nullable=False),
        sa.Column("lens_id", sa.String(length=64), nullable=False),
        sa.Column("jurisdiction", sa.String(length=16), nullable=True),
        sa.Column("title", sa.Text(), nullable=False),
        sa.Column("abstract", sa.Text(), nullable=True),
        sa.Column("full_text", sa.Text(), nullable=True),
        sa.Column("publication_numbers", postgresql.JSONB(astext_type=sa.Text()), nullable=False, server_default=sa.text("'[]'::jsonb")),
        sa.Column("applicants", postgresql.JSONB(astext_type=sa.Text()), nullable=False, server_default=sa.text("'[]'::jsonb")),
        sa.Column("inventors", postgresql.JSONB(astext_type=sa.Text()), nullable=False, server_default=sa.text("'[]'::jsonb")),
        sa.Column("cpc_classes", postgresql.JSONB(astext_type=sa.Text()), nullable=False, server_default=sa.text("'[]'::jsonb")),
        sa.Column("source_url", sa.Text(), nullable=True),
        sa.Column("raw_payload", postgresql.JSONB(astext_type=sa.Text()), nullable=False, server_default=sa.text("'{}'::jsonb")),
        sa.Column("ingested_at", sa.DateTime(timezone=True), server_default=sa.text("now()"), nullable=False),
    )
    op.create_index("ix_patent_documents_lens_id", "patent_documents", ["lens_id"], unique=True)
    op.create_index("ix_patent_documents_jurisdiction", "patent_documents", ["jurisdiction"], unique=False)
    op.create_index("ix_patent_documents_ingested_at", "patent_documents", ["ingested_at"], unique=False)

    op.create_table(
        "patent_chunks",
        sa.Column("id", postgresql.UUID(as_uuid=True), primary_key=True, nullable=False),
        sa.Column("patent_id", postgresql.UUID(as_uuid=True), sa.ForeignKey("patent_documents.id", ondelete="CASCADE"), nullable=False),
        sa.Column("chunk_index", sa.Integer(), nullable=False),
        sa.Column("content", sa.Text(), nullable=False),
        sa.Column("score_hint", sa.Float(), nullable=False, server_default="0"),
        sa.Column("metadata", postgresql.JSONB(astext_type=sa.Text()), nullable=False, server_default=sa.text("'{}'::jsonb")),
        sa.UniqueConstraint("patent_id", "chunk_index", name="uq_patent_chunk_index"),
    )
    op.create_index("ix_patent_chunks_patent_id", "patent_chunks", ["patent_id"], unique=False)


def downgrade() -> None:
    op.drop_index("ix_patent_chunks_patent_id", table_name="patent_chunks")
    op.drop_table("patent_chunks")
    op.drop_index("ix_patent_documents_ingested_at", table_name="patent_documents")
    op.drop_index("ix_patent_documents_jurisdiction", table_name="patent_documents")
    op.drop_index("ix_patent_documents_lens_id", table_name="patent_documents")
    op.drop_table("patent_documents")
