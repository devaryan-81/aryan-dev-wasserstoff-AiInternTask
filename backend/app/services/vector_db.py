print("Qdrant URL:", os.getenv("QDRANT_URL"))
print("Qdrant API Key:", os.getenv("QDRANT_API_KEY"))

import os
import uuid
from typing import List, Dict

from dotenv import load_dotenv
from qdrant_client import QdrantClient
from qdrant_client.http.models import VectorParams, Distance, PointStruct

# Load environment variables from .env file
load_dotenv()

# Retrieve sensitive values from environment
QDRANT_API_KEY = os.getenv("QDRANT_API_KEY")
QDRANT_URL = os.getenv("QDRANT_URL")

# Define the Qdrant collection name
COLLECTION_NAME = "document_embeddings"

# Connect to Qdrant cloud using API key and URL
client = QdrantClient(
    url=QDRANT_URL,
    api_key=QDRANT_API_KEY
)

def init_collection(vector_size: int):
    """
    Initialize the Qdrant collection if it doesn't already exist.
    """
    existing_collections = [c.name for c in client.get_collections().collections]
    
    if COLLECTION_NAME not in existing_collections:
        client.recreate_collection(
            collection_name=COLLECTION_NAME,
            vectors_config=VectorParams(size=vector_size, distance=Distance.COSINE)
        )
        print(f"✅ Created new collection: {COLLECTION_NAME}")
    else:
        print(f"ℹ️ Collection already exists: {COLLECTION_NAME}")

def store_embeddings(document_id: str, text_chunks: List[str], embeddings: List[List[float]]):
    """
    Store text chunks and their embeddings in Qdrant with metadata.

    Args:
        document_id (str): A unique ID for the document.
        text_chunks (List[str]): List of text segments.
        embeddings (List[List[float]]): List of corresponding embeddings.
    """
    points = []

    for i, (chunk, vector) in enumerate(zip(text_chunks, embeddings)):
        point_id = str(uuid.uuid4())  # Generate unique ID
        payload = {
            "document_id": document_id,
            "chunk_index": i,
            "text": chunk
        }

        points.append(PointStruct(
            id=point_id,
            vector=vector,
            payload=payload
        ))

    client.upsert(
        collection_name=COLLECTION_NAME,
        points=points
    )

    print(f"✅ Stored {len(points)} embeddings for document: {document_id}")

def search_similar_chunks(query_embedding: List[float], top_k: int = 5) -> List[Dict]:
    """
    Search the most similar chunks in Qdrant for a given query embedding.

    Args:
        query_embedding (List[float]): Vector for the query.
        top_k (int): Number of top results to return.

    Returns:
        List[Dict]: List of search results with metadata and scores.
    """
    results = client.search(
        collection_name=COLLECTION_NAME,
        query_vector=query_embedding,
        limit=top_k
    )

    return [
        {
            "document_id": hit.payload.get("document_id"),
            "chunk_index": hit.payload.get("chunk_index"),
            "text": hit.payload.get("text"),
            "score": hit.score
        }
        for hit in results
    ]
