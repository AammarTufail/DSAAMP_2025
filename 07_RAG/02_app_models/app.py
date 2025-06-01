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

# --- Available Phi Models ---
PHI_MODELS = [
    "phi3",
    "phi3:mini",
    "phi3:medium",
    "phi3.5",
    "phi3.5:3.8b",
    "phi3.5:latest"
]

# your task is to automat the prcess of running OLLAMA and using it only via streamlit app?

# --- 1. Streamlit Page Config ---
st.set_page_config(page_title="RAG with Ollama (Phi Models)", layout="centered")
st.title("📄🔗 RAG Q&A App with Ollama (Phi Models)")
st.markdown(
    "Upload a PDF or TXT file. Ask questions. Answers are generated using phi models via Ollama."
)

# --- Model Selection ---
selected_model = st.selectbox(
    "🤖 Select Phi Model:",
    PHI_MODELS,
    index=0,
    help="Choose the phi model based on your performance requirements. Smaller models are faster but may be less accurate."
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

# --- 4. Store VectorDB and Model in Streamlit Session State ---
if "vectorstore" not in st.session_state:
    st.session_state.vectorstore = None
if "current_model" not in st.session_state:
    st.session_state.current_model = None

# --- Cleanup Function ---
def cleanup():
    """
    Cleans up temporary files and directories created during the app run.
    """
    if "chroma_dir" in st.session_state:
        chroma_dir = st.session_state.chroma_dir
        if os.path.exists(chroma_dir):
            for root, dirs, files in os.walk(chroma_dir, topdown=False):
                for name in files:
                    os.remove(os.path.join(root, name))
                for name in dirs:
                    os.rmdir(os.path.join(root, name))
            os.rmdir(chroma_dir)  # Remove the main directory

def process_file(uploaded_file, model_name):
    """
    Loads the uploaded document, splits into chunks, embeds using selected phi model,
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

    # Use selected Ollama phi model for embedding text chunks
    embeddings = OllamaEmbeddings(model=model_name)

    # Create a temporary Chroma vector DB directory
    chroma_dir = tempfile.mkdtemp()
    vectordb = Chroma.from_documents(docs, embeddings, persist_directory=chroma_dir)
    return vectordb, chroma_dir

# --- 5. Handle Document Upload ---
if uploaded_file and (st.session_state.vectorstore is None or st.session_state.current_model != selected_model):
    with st.spinner(f"Processing your document with {selected_model} (embedding)..."):
        # Clear existing vectorstore if model changed
        if st.session_state.current_model != selected_model and st.session_state.vectorstore is not None:
            st.session_state.vectorstore = None
            cleanup()
        
        vectordb, chroma_dir = process_file(uploaded_file, selected_model)
        st.session_state.vectorstore = vectordb
        st.session_state.chroma_dir = chroma_dir
        st.session_state.current_model = selected_model
    st.success(f"✅ Document processed with {selected_model}. Ask your questions below!")

# --- 6. Main RAG Q&A Pipeline ---
if query and st.session_state.vectorstore:
    with st.spinner(f"Generating answer with {selected_model}..."):
        llm = Ollama(
            model=selected_model,             # Use selected phi model
            base_url="http://localhost:11434",
            temperature=0.1,                  # Low temp: more factual answers
            # max_tokens=400,                   # Reasonable answer length
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
            st.info(f"Generated using: **{selected_model}**")
            # Show retrieved text chunks as context
            with st.expander("🔎 See retrieved context"):
                for i, doc in enumerate(result['source_documents']):
                    st.markdown(f"**Chunk {i+1}:**\n\n{doc.page_content}")
        except Exception as e:
            st.error(f"Error during QA with {selected_model}: {str(e)}")

# --- 7. Cleanup: Remove temporary files on app exit ---
# Register cleanup function to run on app exit
import atexit
atexit.register(cleanup)
# --- 8. Footer ---
st.markdown("---")