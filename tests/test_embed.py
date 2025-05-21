import os
from app.core.embedding_utils import split_text, embed_text_chunks

def test_split_text_basic():
    sample_text = "This is a sample sentence used for testing the text splitting function. " * 30  # ~300 words
    chunks = split_text(sample_text, max_length=50)

    assert isinstance(chunks, list), "Chunks should be returned in a list"
    assert len(chunks) > 1, "Text should be split into multiple chunks"
    assert all(isinstance(chunk, str) for chunk in chunks), "All chunks must be strings"

def test_split_text_empty():
    chunks = split_text("", max_length=50)
    assert chunks == [], "Empty input should return an empty list"

def test_embed_text_chunks():
    chunks = ["This is chunk one.", "And this is chunk two."]
    embeddings = embed_text_chunks(chunks)

    assert isinstance(embeddings, list), "Embeddings should be a list"
    assert len(embeddings) == len(chunks), "Should return one embedding per chunk"
    assert all(isinstance(vec, list) or hasattr(vec, '__iter__') for vec in embeddings), "Each embedding should be iterable"
    
if __name__ == "__main__":
    test_split_text_basic()
    test_embed_text_chunks()
    print("✅ All embedding tests passed.")

