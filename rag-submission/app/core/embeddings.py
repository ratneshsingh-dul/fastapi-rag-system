from sentence_transformers import SentenceTransformer


class EmbeddingService:

    def __init__(self):

        print("Loading embedding model...")

        self.model = SentenceTransformer(
            "all-MiniLM-L6-v2"
        )

        print("Embedding model loaded!")

    def embed_documents(
        self,
        texts,
    ):

        embeddings = self.model.encode(
            texts
        )

        return embeddings.tolist()

    def embed_query(
        self,
        query,
    ):

        embedding = self.model.encode(
            [query]
        )

        return embedding[0].tolist()


embedding_service = EmbeddingService()


def get_embedding_provider():

    return embedding_service