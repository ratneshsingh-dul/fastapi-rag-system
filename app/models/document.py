from datetime import datetime
import enum

from sqlalchemy import (
    String,
    Integer,
    DateTime,
    Enum,
    Text,
)

from sqlalchemy.orm import (
    Mapped,
    mapped_column,
)

from app.db.database import Base


class DocumentStatus(str, enum.Enum):

    processing = "processing"

    ready = "ready"

    failed = "failed"


class Document(Base):

    __tablename__ = "documents"

    id: Mapped[str] = mapped_column(
        String(36),
        primary_key=True,
    )

    filename: Mapped[str] = mapped_column(
        String(255),
        nullable=False,
    )

    file_type: Mapped[str] = mapped_column(
        String(10),
        nullable=False,
    )

    file_size_bytes: Mapped[int] = mapped_column(
        Integer,
        nullable=False,
    )

    page_count: Mapped[int] = mapped_column(
        Integer,
        default=0,
    )

    chunk_count: Mapped[int] = mapped_column(
        Integer,
        default=0,
    )

    status: Mapped[DocumentStatus] = mapped_column(
        Enum(DocumentStatus),
        default=DocumentStatus.processing,
    )

    error_message: Mapped[str | None] = mapped_column(
        Text,
        nullable=True,
    )

    uploaded_at: Mapped[datetime] = mapped_column(
        DateTime,
        default=datetime.utcnow,
    )

    processed_at: Mapped[datetime | None] = mapped_column(
        DateTime,
        nullable=True,
    )