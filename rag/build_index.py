import os
from rag.document_loader import load_knowledge_base
from rag.chunker import create_chunks

from rag.embeddings import (
    load_embedding_model,
    create_embeddings
)

from rag.vector_store import (
    create_faiss_index,
    save_faiss_index
)

KNOWLEDGE_BASE = "data/knowledge_base"


OUTPUT_FOLDER = "data/processed/rag_index"


print("=" * 60)
print("CAREERPILOT AI - BUILDING RAG INDEX")
print("=" * 60)


# Step 1: Load documents
documents = load_knowledge_base(
    KNOWLEDGE_BASE
)

print(
    "Documents loaded:",
    len(documents)
)


# Step 2: Create chunks
chunks = create_chunks(
    documents
)

print(
    "Chunks created:",
    len(chunks)
)


# Step 3: Load embedding model
model = load_embedding_model()


# Step 4: Extract chunk text
texts = [
    chunk["text"]
    for chunk in chunks
]


# Step 5: Generate embeddings
embeddings = create_embeddings(
    texts,
    model
)


print(
    "Embedding shape:",
    embeddings.shape
)


# Step 6: Build FAISS index
index = create_faiss_index(
    embeddings
)


# Step 7: Save
save_faiss_index(
    index,
    chunks,
    OUTPUT_FOLDER
)


print("\nRAG index created successfully!")