from rag.embeddings import load_embedding_model
from rag.vector_store import load_faiss_index


# ============================================================
# PATHS
# ============================================================

INDEX_PATH = "data/processed/rag_index/career_index.faiss"
CHUNKS_PATH = "data/processed/rag_index/chunks.pkl"


# ============================================================
# RAG RETRIEVER
# ============================================================

class RAGRetriever:

    def __init__(self):

        print("Loading RAG embedding model...")

        self.model = load_embedding_model()

        print("Loading FAISS index...")

        self.index, self.chunks = load_faiss_index(
            INDEX_PATH,
            CHUNKS_PATH
        )

        print("RAG index loaded successfully.")


    # ========================================================
    # RETRIEVE
    # ========================================================

    def retrieve(
        self,
        query,
        top_k=5
    ):

        return self.search(
            query,
            top_k
        )


    # ========================================================
    # SEARCH
    # ========================================================

    def search(
        self,
        query,
        top_k=5
    ):

        # Convert query into embedding
        query_embedding = self.model.encode(
            [query],
            convert_to_numpy=True
        )

        # FAISS expects float32
        query_embedding = query_embedding.astype(
            "float32"
        )

        # Search FAISS
        distances, indices = self.index.search(
            query_embedding,
            top_k
        )

        results = []

        # Process search results
        for distance, index in zip(
            distances[0],
            indices[0]
        ):

            if index < 0:
                continue

            if index < len(self.chunks):

                result = self.chunks[index].copy()

                result["distance"] = float(
                    distance
                )

                results.append(
                    result
                )

        return results


# ============================================================
# BUILD CONTEXT
# ============================================================

def build_context(results):

    context_parts = []

    for result in results:

        source = result.get(
            "source",
            "Unknown"
        )

        text = result.get(
            "text",
            ""
        )

        context_parts.append(
            f"Source: {source}\n"
            f"{text}"
        )

    return "\n\n".join(
        context_parts
    )