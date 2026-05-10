import chromadb

from sentence_transformers import (
    SentenceTransformer
)

# -----------------------------
# EMBEDDING MODEL
# -----------------------------
embedding_model = (
    SentenceTransformer(
        "all-MiniLM-L6-v2"
    )
)

# -----------------------------
# CHROMA DB
# -----------------------------
client = chromadb.PersistentClient(
    path="./chroma_db"
)

collection = (
    client.get_or_create_collection(
        name="memory_collection"
    )
)


# -----------------------------
# STORE MEMORY
# -----------------------------
def store_memory(memory_text):

    embedding = (
        embedding_model.encode(
            memory_text
        ).tolist()
    )

    collection.add(
        documents=[memory_text],
        embeddings=[embedding],
        ids=[str(hash(memory_text))]
    )


# -----------------------------
# RETRIEVE MEMORIES
# -----------------------------
def retrieve_relevant_memories(query):

    try:

        query_embedding = (
            embedding_model.encode(
                query
            ).tolist()
        )

        results = collection.query(
            query_embeddings=[
                query_embedding
            ],
            n_results=3
        )

        return results["documents"][0]

    except:
        return []