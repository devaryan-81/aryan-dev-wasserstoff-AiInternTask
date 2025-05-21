import streamlit as st
import requests

st.set_page_config(page_title="Document Research & Theme Bot", layout="wide")

API_URL = "http://127.0.0.1:8000"


st.title("📚 Document Research & Theme Identifier")

st.sidebar.markdown("### 📤 Upload Documents")
uploaded_files = st.sidebar.file_uploader(
    "Upload multiple PDF or image files", type=["pdf", "jpg", "jpeg", "png"], accept_multiple_files=True
)
if st.sidebar.button("Upload to Knowledge Base"):
    if uploaded_files:
        files = [("files", (f.name, f.read(), "application/octet-stream")) for f in uploaded_files]
        res = requests.post(f"{API_URL}/upload-batch", files=files)
        if res.status_code == 200:
            st.sidebar.success("Uploaded successfully!")
            st.json(res.json())
        else:
            st.sidebar.error("Upload failed")
    else:
        st.sidebar.warning("No files selected.")

st.markdown("---")
tab1, tab2 = st.tabs(["🔍 Semantic Search", "🧠 Extract Themes"])

# Query Tab
with tab1:
    st.subheader("Ask a question about uploaded documents")
    query = st.text_input("Your question:")
    if st.button("Search"):
        if query.strip():
            res = requests.post(f"{API_URL}/query", json={"query": query})
            if res.ok:
                results = res.json().get("results", [])
                for r in results:
                    st.markdown(f"**📄 Document:** `{r['document_id']}`")
                    st.markdown(f"> {r['text']}")
                    st.markdown("---")
            else:
                st.error("Query failed. Check backend.")
        else:
            st.warning("Enter a question to search.")

# Theme Tab
with tab2:
    st.subheader("Ask a high-level query to extract themes")
    theme_query = st.text_input("Enter your thematic question:")
    if st.button("Extract Themes"):
        if theme_query.strip():
            res = requests.post(f"{API_URL}/themes", json={"query": theme_query})
            if res.ok:
                themes = res.json().get("themes", [])
                for idx, t in enumerate(themes):
                    st.markdown(f"### 🧩 Theme {idx+1}")
                    st.markdown(f"**Summary:** {t['theme']}")
                    st.markdown(f"📎 Supports: {', '.join(t['supporting_documents'])}")
                    st.markdown("---")
            else:
                st.error("Theme extraction failed.")
        else:
            st.warning("Enter a high-level question to extract themes.")

st.markdown("---")
if st.button("📋 View Uploaded Documents"):
    res = requests.get(f"{API_URL}/documents")
    if res.ok:
        docs = res.json().get("documents", [])
        st.json(docs)
    else:
        st.error("Failed to load document list")
