from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from contextlib import asynccontextmanager

from app.api import documents, query, health
from app.db.database import init_db


@asynccontextmanager
async def lifespan(app: FastAPI):
    await init_db()
    yield


app = FastAPI(
    title="Enterprise RAG Pipeline",
    version="1.0.0",
    lifespan=lifespan,
)


app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


app.include_router(
    health.router,
    prefix="/api/v1",
    tags=["Health"],
)

app.include_router(
    documents.router,
    prefix="/api/v1/documents",
    tags=["Documents"],
)

app.include_router(
    query.router,
    prefix="/api/v1/query",
    tags=["Query"],
)


@app.get("/")
async def root():
    return {
        "message": "Enterprise RAG Pipeline",
        "docs": "/docs",
    }