import uuid
from app.services.vector_db import store_embeddings, search_similar_chunks, init_collection

def test_qdrant_storage_and_search():
    # Sample document ID
    doc_id = f"test-doc-{uuid.uuid4()}"

    # Sample text chunks
    chunks = [
        "Artificial Intelligence is transforming industries.",
        "Large Language Models like GPT are powerful.",
        "Qdrant is a vector search engine for AI applications."
    ]

    # Sample dummy embeddings (same length as expected by embedding model)
    # e.g., all-MiniLM-L6-v2 returns 384-dim vectors
    dummy_embedding = [0.01] * 384
    embeddings = [dummy_embedding for _ in chunks]

    # Step 1: Create the collection if not exists
    init_collection(vector_size=384)

    # Step 2: Store sample embeddings
    store_embeddings(doc_id, chunks, embeddings)

    # Step 3: Perform a search with one of the dummy embeddings
    results = search_similar_chunks(dummy_embedding, top_k=2)

    assert isinstance(results, list), "Search result should be a list"
    assert len(results) > 0, "Should return at least one match"
    assert "text" in results[0], "Each result should contain matched text"
    assert results[0]["document_id"] == doc_id, "Result should match document_id"

    print("✅ Qdrant test passed. Top result:", results[0]["text"])

if __name__ == "__main__":
    test_qdrant_storage_and_search()
    print("✅ All Qdrant storage + search tests passed.")
