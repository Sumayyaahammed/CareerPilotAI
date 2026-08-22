import os

from embeddings import load_embedding_model
from vector_store import load_faiss_index


INDEX_PATH = "../data/processed/rag_index/career_index.faiss"

CHUNKS_PATH = "../data/processed/rag_index/chunks.pkl"


class RAGRetriever:

    def __init__(self):

        self.model = load_embedding_model()

        self.index, self.chunks = load_faiss_index(
            INDEX_PATH,
            CHUNKS_PATH
        )


    def search(
        self,
        query,
        top_k=5
    ):

        query_embedding = self.model.encode(
            [query]
        )

        distances, indices = self.index.search(
            query_embedding,
            top_k
        )

        results = []

        for distance, index in zip(
            distances[0],
            indices[0]
        ):

            if index < len(self.chunks):

                result = self.chunks[index].copy()

                result["distance"] = float(
                    distance
                )

                results.append(result)

        return results

def build_context(results):

    context_parts = []

    for result in results:

        context_parts.append(
            f"Source: {result['source']}\n"
            f"{result['text']}"
        )

    return "\n\n".join(
        context_parts
    )