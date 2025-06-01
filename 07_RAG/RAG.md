# 🦙 Streamlit RAG App with Ollama (phi3 Model)

## Overview

This guide shows you how to build a **Retrieval-Augmented Generation (RAG)** app using:
- [Streamlit](https://streamlit.io) for a web interface
- [Ollama](https://ollama.com) to run a local LLM (`phi3`, a lightweight model)
- [LangChain](https://python.langchain.com/) for document retrieval and chaining
- [Chroma](https://www.trychroma.com/) as the local vector database

You can upload a PDF or text file and ask questions—your local AI will answer using information from your document!

---

## Prerequisites

- **Windows 10/11** (works on Linux/Mac too)
- **Python 3.9+**
- **Ollama installed and running**
- **Internet for first setup**

---

## Installation

1. **Install Python dependencies**

```bash
conda create -n rag_env python=3.10 -y
conda activate rag_env
pip install streamlit langchain chromadb pypdf ollama requests

2.	Install and launch Ollama
Download Ollama: https://ollama.com/download
After installation, open a terminal and run:

ollama run phi3

This will pull and start the lightweight phi3 model locally.

⸻

Usage
	1.	Save the app code (below) as rag_ollama_app.py
	2.	Run the Streamlit app:

streamlit run rag_ollama_app.py


	3.	Open your browser to http://localhost:8501
	4.	Upload your document and ask questions!

⸻

Code with Annotations

# --- Imports: Core libraries for the app ---
import streamlit as st                           # For web UI
import os
import tempfile                                 # For temporary file handling
import requests                                 # To check if Ollama server is running

# --- LangChain & dependencies for RAG pipeline ---
from langchain.document_loaders import PyPDFLoader, TextLoader      # For loading PDF/TXT files
from langchain.embeddings import OllamaEmbeddings                   # To embed text using Ollama models
from langchain.vectorstores import Chroma                           # To store and search embeddings
from langchain.llms import Ollama                                   # For connecting to Ollama LLM
from langchain.chains import RetrievalQA                            # LangChain chain for RAG

# --- 1. Streamlit Page Config ---
st.set_page_config(page_title="RAG with Ollama (Lightweight)", layout="centered")
st.title("📄🔗 RAG Q&A App with Ollama (phi3)")
st.markdown(
    "Upload a PDF or TXT file. Ask questions. Answers are generated using the lightweight [phi3](https://ollama.com/library/phi3) model via Ollama."
)

# --- 2. Ollama Status Check ---
def is_ollama_running():
    """
    Checks if Ollama server is up and running at localhost:11434.
    If not running, shows an error and stops the app.
    """
    try:
        r = requests.get("http://localhost:11434")
        return r.status_code == 200
    except Exception:
        return False

if not is_ollama_running():
    st.error(
        "Ollama is not running! Please open a terminal and run:\n\n"
        "`ollama run phi3`\n\nThen restart this app."
    )
    st.stop()   # Stop app if Ollama isn't running

# --- 3. User Inputs: File upload and question ---
uploaded_file = st.file_uploader("Upload your PDF or TXT file", type=["pdf", "txt"])
query = st.text_input("Ask a question about your document:")

# --- 4. Store VectorDB in Streamlit Session State ---
if "vectorstore" not in st.session_state:
    st.session_state.vectorstore = None

def process_file(uploaded_file):
    """
    Loads the uploaded document, splits into chunks, embeds using phi3,
    and builds a Chroma vector DB.
    """
    suffix = "." + uploaded_file.name.split(".")[-1]
    # Save uploaded file to a temporary file
    with tempfile.NamedTemporaryFile(delete=False, suffix=suffix) as tmp:
        tmp.write(uploaded_file.read())
        file_path = tmp.name

    # Choose loader based on file extension
    if file_path.endswith(".pdf"):
        loader = PyPDFLoader(file_path)
    else:
        loader = TextLoader(file_path)

    docs = loader.load_and_split()  # Split doc into small text chunks

    # Use Ollama phi3 model for embedding text chunks
    embeddings = OllamaEmbeddings(model="phi3")  # Lightweight & fast

    # Create a temporary Chroma vector DB directory
    chroma_dir = tempfile.mkdtemp()
    vectordb = Chroma.from_documents(docs, embeddings, persist_directory=chroma_dir)
    return vectordb, chroma_dir

# --- 5. Handle Document Upload ---
if uploaded_file and st.session_state.vectorstore is None:
    with st.spinner("Processing your document (embedding)..."):
        vectordb, chroma_dir = process_file(uploaded_file)
        st.session_state.vectorstore = vectordb
        st.session_state.chroma_dir = chroma_dir
    st.success("✅ Document processed. Ask your questions below!")

# --- 6. Main RAG Q&A Pipeline ---
if query and st.session_state.vectorstore:
    with st.spinner("Generating answer with phi3..."):
        llm = Ollama(
            model="phi3",                     # Use phi3, the lightweight LLM
            base_url="http://localhost:11434",
            temperature=0.1,                  # Low temp: more factual answers
            max_tokens=400,                   # Reasonable answer length
        )
        # LangChain RetrievalQA: combines retrieval with LLM generation
        qa_chain = RetrievalQA.from_chain_type(
            llm=llm,
            chain_type="stuff",               # Simple retrieval
            retriever=st.session_state.vectorstore.as_retriever(),
            return_source_documents=True      # Show which doc chunks were used
        )
        try:
            result = qa_chain(query)
            st.subheader("💡 Answer")
            st.write(result["result"])
            # Show retrieved text chunks as context
            with st.expander("🔎 See retrieved context"):
                for i, doc in enumerate(result['source_documents']):
                    st.markdown(f"**Chunk {i+1}:**\n\n{doc.page_content}")
        except Exception as e:
            st.error(f"Error during QA: {str(e)}")

# --- 7. (Optional) Cleanup: Remove temp files/DBs if you wish ---

st.markdown("---")
st.markdown(
    "Lightweight and local — everything stays on your computer. Powered by [Ollama](https://ollama.com) and [LangChain](https://python.langchain.com/)."
)


⸻

Troubleshooting
	•	Ollama not running?
Open a terminal and run:
ollama run phi3
	•	No answer or slow response?
	•	Ensure Ollama has finished downloading the model.
	•	Try restarting the Streamlit app.
	•	For large PDFs, allow a few extra seconds for embedding.
	•	Use a different model:
Change "phi3" in the code to any other model name you have pulled with Ollama (e.g., "llama2", "mistral", etc.)

⸻

Notes & Customization
	•	Supports both PDF and TXT files.
	•	Local only: All files and processing are local, no cloud or data leak.
	•	Vector DB is temporary: New upload creates a new vector store.
	•	Advanced features: You can add authentication, history, multi-file support, chat mode, or Markdown rendering.

⸻

Credits
	•	Ollama
	•	LangChain
	•	ChromaDB
	•	Streamlit

⸻
