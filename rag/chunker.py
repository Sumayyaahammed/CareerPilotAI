def chunk_text(
    text,
    chunk_size=800,
    overlap=100
):
    """
    Split text into overlapping chunks.
    """

    words = text.split()

    chunks = []

    start = 0

    while start < len(words):

        end = start + chunk_size

        chunk = " ".join(
            words[start:end]
        )

        if chunk.strip():
            chunks.append(chunk)

        start += chunk_size - overlap

    return chunks

def create_chunks(documents):

    all_chunks = []

    for document in documents:

        chunks = chunk_text(
            document["text"]
        )

        for index, chunk in enumerate(chunks):

            all_chunks.append({
                "text": chunk,
                "source": document["source"],
                "chunk_id": index
            })

    return all_chunks