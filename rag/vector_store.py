import os
import pickle

import faiss
import numpy as np


def create_faiss_index(embeddings):

    embeddings = np.asarray(
        embeddings,
        dtype="float32"
    )

    dimension = embeddings.shape[1]

    index = faiss.IndexFlatL2(
        dimension
    )

    index.add(embeddings)

    return index



def save_faiss_index(
    index,
    chunks,
    output_folder
):

    os.makedirs(
        output_folder,
        exist_ok=True
    )

    faiss.write_index(
        index,
        os.path.join(
            output_folder,
            "career_index.faiss"
        )
    )

    with open(
        os.path.join(
            output_folder,
            "chunks.pkl"
        ),
        "wb"
    ) as file:

        pickle.dump(
            chunks,
            file
        )


def load_faiss_index(
    index_path,
    chunks_path
):

    index = faiss.read_index(
        index_path
    )

    with open(
        chunks_path,
        "rb"
    ) as file:

        chunks = pickle.load(file)

    return index, chunks