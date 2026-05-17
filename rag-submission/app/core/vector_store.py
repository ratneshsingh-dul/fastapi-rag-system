from typing import List, Dict
from functools import lru_cache

import faiss
import numpy as np

from app.core.embeddings import (
    get_embedding_provider,
)


class FAISSVectorStore:

    def __init__(self):

        self.embedder = get_embedding_provider()

        self.index = None

        self.texts = []

        self.metadatas = []

    def upsert(
        self,
        doc_id: str,
        chunks: List[str],
        metadatas: List[Dict],
    ):

        embeddings = self.embedder.embed_documents(
            chunks
        )

        arr = np.array(
            embeddings,
            dtype="float32",
        )

        faiss.normalize_L2(arr)

        if self.index is None:

            dim = arr.shape[1]

            self.index = faiss.IndexFlatIP(dim)

        self.index.add(arr)

        self.texts.extend(chunks)

        self.metadatas.extend(metadatas)

    def search(
        self,
        query: str,
        top_k: int = 5,
    ):

        if self.index is None:
            return []

        query_embedding = self.embedder.embed_query(
            query
        )

        q = np.array(
            [query_embedding],
            dtype="float32",
        )

        faiss.normalize_L2(q)

        scores, indices = self.index.search(
            q,
            top_k,
        )

        results = []

        for score, idx in zip(
            scores[0],
            indices[0],
        ):

            if idx < 0:
                continue

            results.append({
                "text": self.texts[idx],
                "metadata": self.metadatas[idx],
                "score": float(score),
            })

        return results

    def delete_document(
        self,
        doc_id: str,
    ):

        pass


@lru_cache(maxsize=1)
def get_vector_store():

    return FAISSVectorStore()