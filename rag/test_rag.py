
from query_engine import (
    RAGRetriever,
    build_context
)


retriever = RAGRetriever()


query = "What skills are required to become a data scientist?"


results = retriever.search(
    query,
    top_k=5
)


context = build_context(
    results
)


print("=" * 60)
print("RETRIEVED CONTEXT")
print("=" * 60)

print(context)