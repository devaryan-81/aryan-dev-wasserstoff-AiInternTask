from sentence_transformers import SentenceTransformer
from typing import List

# Load the SentenceTransformer model once when the file is imported
model = SentenceTransformer('all-MiniLM-L6-v2')

def split_text(text: str, max_length: int = 512) -> List[str]:
    """
    Split text into smaller chunks of max token length.
    
    Args:
        text (str): The full document text.
        max_length (int): Max number of words per chunk.

    Returns:
        List[str]: List of smaller text chunks.
    """
    words = text.split()  # Split full text into words
    chunks = []

    for i in range(0, len(words), max_length):
        chunk = " ".join(words[i:i + max_length])  # Group into chunks
        chunks.append(chunk)

    return chunks


def embed_text_chunks(chunks: List[str]) -> List[List[float]]:
    """
    Convert text chunks to embeddings using SentenceTransformer.
    
    Args:
        chunks (List[str]): List of text segments.
    
    Returns:
        List[List[float]]: Corresponding list of embeddings.
    """
    embeddings = model.encode(chunks, show_progress_bar=True)
    return embeddings.tolist()
