from fastapi import (
    APIRouter,
    HTTPException,
    Depends,
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
    QueryRequest,
    QueryResponse,
    SourceChunk,
)

from app.core.vector_store import (
    get_vector_store,
)

from app.core.llm import (
    get_llm,
)


router = APIRouter()


@router.post(
    "",
    response_model=QueryResponse,
)
async def query_documents(
    request: QueryRequest,
    db: AsyncSession = Depends(get_db),
):

    if not request.query.strip():

        raise HTTPException(
            400,
            "Query cannot be empty",
        )

    result = await db.execute(
        select(Document).where(
            Document.status == DocumentStatus.ready
        )
    )

    docs = result.scalars().all()

    if not docs:

        raise HTTPException(
            400,
            "No ready documents available",
        )

    vs = get_vector_store()

    raw_chunks = vs.search(
        query=request.query,
        top_k=request.top_k,
    )

    if not raw_chunks:

        return QueryResponse(
            query=request.query,
            answer="No relevant information found",
            sources=[],
        )

    llm = get_llm()

    answer = llm.generate(
        query=request.query,
        context_chunks=raw_chunks,
    )

    sources = []

    for chunk in raw_chunks:

        sources.append(
            SourceChunk(
                text=chunk["text"][:400],
                filename=chunk["metadata"].get(
                    "filename"
                ),
                chunk_index=chunk["metadata"].get(
                    "chunk_index"
                ),
                score=chunk["score"],
            )
        )

    return QueryResponse(
        query=request.query,
        answer=answer,
        sources=sources,
    )