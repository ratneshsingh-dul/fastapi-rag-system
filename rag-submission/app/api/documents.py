import uuid

from datetime import datetime
from pathlib import Path

from fastapi import (
    APIRouter,
    UploadFile,
    File,
    HTTPException,
    Depends,
    BackgroundTasks,
)

from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select

from app.db.database import (
    get_db,
)

from app.models.document import (
    Document,
    DocumentStatus,
)

from app.models.schemas import (
    DocumentResponse,
    DocumentListResponse,
)

from app.core.document_processor import (
    extract_text,
    chunk_text,
)

from app.core.vector_store import (
    get_vector_store,
)


router = APIRouter()

ALLOWED_EXTENSIONS = {
    ".pdf",
    ".docx",
    ".txt",
    ".md",
}


async def _process_document(
    doc_id: str,
    filename: str,
    content: bytes,
):

    from app.db.database import (
        AsyncSessionLocal,
    )

    async with AsyncSessionLocal() as db:

        doc = await db.get(
            Document,
            doc_id,
        )

        if not doc:
            return

        try:

            print("Starting document processing...")

            text, page_count = extract_text(
                filename,
                content,
            )

            print("Text extracted successfully")

            chunks = chunk_text(text)

            print(f"Generated {len(chunks)} chunks")

            metadatas = []

            for i in range(len(chunks)):

                metadatas.append({
                    "doc_id": doc_id,
                    "filename": filename,
                    "chunk_index": i,
                })

            vs = get_vector_store()

            print("Adding embeddings to vector store...")

            vs.upsert(
                doc_id,
                chunks,
                metadatas,
            )

            print("Vector store updated successfully")

            doc.page_count = page_count

            doc.chunk_count = len(chunks)

            doc.status = DocumentStatus.ready

            doc.processed_at = datetime.utcnow()

            print("Document marked as ready")

        except Exception as e:

            print("PROCESSING ERROR:", e)

            import traceback
            traceback.print_exc()

            doc.status = DocumentStatus.failed

            doc.error_message = str(e)

        await db.commit()


@router.post(
    "/upload",
    response_model=DocumentResponse,
    status_code=201,
)
async def upload_document(
    background_tasks: BackgroundTasks,
    file: UploadFile = File(...),
    db: AsyncSession = Depends(get_db),
):

    if not file.filename:
        raise HTTPException(
            400,
            "Filename missing",
        )

    ext = Path(file.filename).suffix.lower()

    if ext not in ALLOWED_EXTENSIONS:
        raise HTTPException(
            400,
            "Unsupported file type",
        )

    content = await file.read()

    doc_id = str(uuid.uuid4())

    doc = Document(
        id=doc_id,
        filename=file.filename,
        file_type=ext,
        file_size_bytes=len(content),
        status=DocumentStatus.processing,
    )

    db.add(doc)

    await db.commit()

    await db.refresh(doc)

    background_tasks.add_task(
        _process_document,
        doc_id,
        file.filename,
        content,
    )

    return doc


@router.get(
    "",
    response_model=DocumentListResponse,
)
async def list_documents(
    db: AsyncSession = Depends(get_db),
):

    result = await db.execute(
        select(Document)
    )

    docs = result.scalars().all()

    return {
        "documents": docs,
        "total": len(docs),
    }


@router.get(
    "/{doc_id}",
    response_model=DocumentResponse,
)
async def get_document(
    doc_id: str,
    db: AsyncSession = Depends(get_db),
):

    doc = await db.get(
        Document,
        doc_id,
    )

    if not doc:
        raise HTTPException(
            404,
            "Document not found",
        )

    return doc


@router.delete(
    "/{doc_id}",
    status_code=204,
)
async def delete_document(
    doc_id: str,
    db: AsyncSession = Depends(get_db),
):

    doc = await db.get(
        Document,
        doc_id,
    )

    if not doc:
        raise HTTPException(
            404,
            "Document not found",
        )

    await db.delete(doc)

    await db.commit()