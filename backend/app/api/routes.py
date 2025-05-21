
from fastapi import APIRouter, File, UploadFile, HTTPException
from fastapi.responses import JSONResponse
from typing import List
import uuid
import os
import json

from app.models.schemas import QueryRequest
from app.core.pdf_utils import extract_text_from_pdf
from app.core.ocr_utils import extract_text_from_image
from app.core.embedding_utils import split_text, embed_text_chunks
from app.services.vector_db import store_embeddings, init_collection, search_similar_chunks

from sklearn.cluster import KMeans
import numpy as np
import openai
from PyPDF2 import PdfReader

router = APIRouter()

UPLOAD_DIR = "backend/data/uploads"
METADATA_FILE = "backend/data/metadata.json"

os.makedirs(UPLOAD_DIR, exist_ok=True)
if not os.path.exists(METADATA_FILE):
    with open(METADATA_FILE, "w") as f:
        f.write("[]")

openai.api_key = os.getenv("OPENAI_API_KEY")

def save_uploaded_file(file: UploadFile) -> str:
    file_ext = os.path.splitext(file.filename)[1].lower()
    unique_filename = f"{uuid.uuid4()}{file_ext}"
    file_path = os.path.join(UPLOAD_DIR, unique_filename)

    with open(file_path, "wb") as f:
        f.write(file.file.read())
    file.file.close()


    return file_path

def save_document_metadata(entry: dict):
    with open(METADATA_FILE, "r+") as f:
        try:
            data = json.load(f)
        except:
            data = []
        data.append(entry)
        f.seek(0)
        json.dump(data, f, indent=2)


@router.post("/upload")
async def upload_file(file: UploadFile = File(...)):
    try:
        file_path = save_uploaded_file(file)

        if file.filename.endswith(".pdf"):
            text = extract_text_from_pdf(file_path)
        elif file.filename.lower().endswith((".jpg", ".jpeg", ".png")):
            text = extract_text_from_image(file_path)
        else:
            raise HTTPException(status_code=400, detail="Unsupported file type")

        if not text:
            raise HTTPException(status_code=422, detail="No text extracted from file")

        chunks = split_text(text)
        embeddings = embed_text_chunks(chunks)

        init_collection(vector_size=len(embeddings[0]))
        document_id = str(uuid.uuid4())
        store_embeddings(document_id, chunks, embeddings)

        save_document_metadata({
            "document_id": document_id,
            "filename": file.filename,
            "chunks": len(chunks)
        })

        return JSONResponse({
            "message": "File processed and embeddings stored",
            "document_id": document_id,
            "total_chunks": len(chunks)
        })

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/upload-batch")
async def upload_multiple_files(files: List[UploadFile] = File(...)):
    results = []

    for file in files:
        try:
            file_path = save_uploaded_file(file)

            if file.filename.endswith(".pdf"):
                text = extract_text_from_pdf(file_path)
            elif file.filename.lower().endswith((".jpg", ".jpeg", ".png")):
                text = extract_text_from_image(file_path)
            else:
                raise Exception("Unsupported file type")

            if not text:
                raise Exception("No text extracted")

            chunks = split_text(text)
            embeddings = embed_text_chunks(chunks)

            init_collection(vector_size=len(embeddings[0]))
            doc_id = str(uuid.uuid4())
            store_embeddings(doc_id, chunks, embeddings)

            save_document_metadata({
                "document_id": doc_id,
                "filename": file.filename,
                "chunks": len(chunks)
            })

            results.append({
                "filename": file.filename,
                "document_id": doc_id,
                "total_chunks": len(chunks)
            })

        except Exception as e:
            results.append({
                "filename": file.filename,
                "error": str(e)
            })

    return {"uploaded_documents": results}


@router.post("/query")
async def query_document(req: QueryRequest):
    try:
        query = req.query.strip()
        if not query:
            raise HTTPException(status_code=400, detail="Query cannot be empty")

        query_vector = embed_text_chunks([query])[0]
        top_results = search_similar_chunks(query_vector, top_k=5)

        return {"results": top_results}

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/documents")
async def list_documents():
    try:
        with open(METADATA_FILE, "r") as f:
            data = json.load(f)
        return {"documents": data}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/themes")
async def identify_themes(req: QueryRequest):
    try:
        query = req.query.strip()
        if not query:
            raise HTTPException(status_code=400, detail="Query cannot be empty")

        query_vector = embed_text_chunks([query])[0]
        results = search_similar_chunks(query_vector, top_k=15)

        texts = [r["text"] for r in results]
        embeddings = embed_text_chunks(texts)

        kmeans = KMeans(n_clusters=min(3, len(embeddings)), random_state=42)
        labels = kmeans.fit_predict(embeddings)

        clustered = {}
        for label, res in zip(labels, results):
            clustered.setdefault(label, []).append(res)

        themes = []
        for label, group in clustered.items():
            group_texts = "\n".join([item["text"] for item in group])
            document_ids = list(set([item["document_id"] for item in group]))

            completion = openai.ChatCompletion.create(
                model="gpt-3.5-turbo",
                messages=[
                    {"role": "system", "content": "You are a helpful summarizer."},
                    {"role": "user", "content": f"Summarize the following into a theme:\n\n{group_texts}"}
                ]
            )

            summary = completion.choices[0].message.content.strip()

            themes.append({
                "theme": summary,
                "supporting_documents": document_ids
            })

        return {"themes": themes}

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
