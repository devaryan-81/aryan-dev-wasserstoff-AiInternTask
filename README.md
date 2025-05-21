# 🧠 Document Research & Theme Identifier Chatbot

A smart AI-powered system that allows you to upload scanned PDFs/images, extract semantic information, query documents with citations, and identify cross-document themes. Built with **FastAPI** (backend) and **Streamlit** (frontend).

---

## 🚀 Features

- 📤 Upload multiple documents (PDFs or images)
- 🧾 Extract scanned text using OCR (Tesseract)
- 🔍 Query the documents in natural language
- 🧠 Identify common themes across multiple documents
- 📄 Citations with document IDs for traceability
- 🌐 Interactive Streamlit frontend

---

## 🧰 Tech Stack

| Layer       | Technology            |
|-------------|------------------------|
| Backend     | FastAPI + Uvicorn     |
| OCR         | Tesseract OCR          |
| PDF Images  | pdf2image              |
| Embedding   | Sentence Transformers  |
| Vector DB   | Qdrant                 |
| Clustering  | scikit-learn (KMeans)  |
| Frontend    | Streamlit              |

---

## 📁 Project Structure

```
AiInternTask/
├── backend/
│   ├── app/
│   │   ├── api/routes.py
│   │   ├── core/
│   │   ├── models/
│   │   └── main.py
│   ├── data/uploads/
│   ├── requirements.txt
│   └── .env.example
├── streamlit_app/
│   └── app.py
├── tests/
│   └── test_embed.py, test_vector_db.py
├── README.md
└── .gitignore
```

---

## 🛠 Setup Instructions

### 1. Clone the repository
```bash
git clone https://github.com/aryan-dev/wasserstoff/AiInternTask.git
cd AiInternTask
```

### 2. Setup virtual environment
```bash
python -m venv .venv
.\.venv\Scriptsctivate
pip install -r backend/requirements.txt
```

### 3. Configure environment variables
Create `.env` in `backend/`:
```
OPENAI_API_KEY=your-openai-key
QDRANT_HOST=http://localhost:6333
```

### 4. Start the backend
```bash
cd backend
uvicorn app.main:app --reload
```

### 5. Start the frontend
```bash
cd ../streamlit_app
streamlit run app.py
```

---

## 🌐 Hosted App

Live demo (via Streamlit Cloud or HuggingFace):  
🔗 https://aryan-dev-wasserstoff-aiinterntask-7vkq4kdgappn6fsxdzrnqyo.streamlit.app

---

## 🧪 Sample API Routes

| Endpoint       | Method | Description                      |
|----------------|--------|----------------------------------|
| `/upload`      | POST   | Upload a single file             |
| `/upload-batch`| POST   | Upload multiple files            |
| `/query`       | POST   | Ask a question on the documents  |
| `/themes`      | POST   | Get theme summary across docs    |
| `/documents`   | GET    | List uploaded documents          |

---

## 🧪 Sample Query Result

```
{
  "results": [
    {
      "document_id": "DOC001",
      "text": "The order states that the fine was imposed under section 15 of the SEBI Act."
    }
  ]
}
```

---

## 📽️ Submission Guidelines

- [x] Public GitHub repo: `aryan-dev/wasserstoff/AiInternTask`
- [x] Well-commented and modular code
- [x] Hosted app via Streamlit Cloud / HuggingFace Spaces
- [x] `.env.example` and test cases included
- [x] Demonstration-ready interface

---

## 🤝 Credits

Built for Wasserstoff Gen-AI Internship Challenge — May 2025.  
Developed by Aryan Dev 🚀
