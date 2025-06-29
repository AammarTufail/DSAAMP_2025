import os
import ssl
import urllib3
import warnings

# Must be set before any other imports
os.environ['PYTHONHTTPSVERIFY'] = '0'  # Disables HTTPS certificate verification for Python
os.environ['CURL_CA_BUNDLE'] = ''      # Unsets CURL CA bundle to avoid SSL issues
os.environ['REQUESTS_CA_BUNDLE'] = ''  # Unsets Requests CA bundle to avoid SSL issues

# Comprehensive telemetry disabling
os.environ['LANGCHAIN_TRACING_V2'] = 'false'      # Disables LangChain tracing v2
os.environ['LANGCHAIN_TELEMETRY'] = 'false'       # Disables LangChain telemetry
os.environ['LANGSMITH_TRACING'] = 'false'         # Disables LangSmith tracing
os.environ['LANGCHAIN_ANALYTICS'] = 'false'       # Disables LangChain analytics
os.environ['LANGCHAIN_CALLBACKS_MANAGER'] = 'false' # Disables LangChain callbacks manager
os.environ['LANGCHAIN_VERBOSE'] = 'false'         # Disables verbose logging
os.environ['LANGCHAIN_DEBUG'] = 'false'           # Disables debug logging

# Suppress all warnings including telemetry warnings
warnings.filterwarnings("ignore")  # Ignores all Python warnings

# Remove SSL_CERT_FILE if it exists and is causing issues
if 'SSL_CERT_FILE' in os.environ:
    del os.environ['SSL_CERT_FILE']  # Removes SSL_CERT_FILE from environment if present

# Disable SSL warnings and configure SSL context
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)  # Disables urllib3 SSL warnings

# Configure SSL context to be more permissive
ssl._create_default_https_context = ssl._create_unverified_context  # Disables SSL certificate verification globally

# Now import the other modules
from langchain_ollama import OllamaEmbeddings  # Import Ollama embeddings for vectorization
from langchain_chroma import Chroma            # Import Chroma vector store
from langchain_core.documents import Document  # Import Document class for storing text and metadata
import pandas as pd                            # Import pandas for data manipulation

df = pd.read_csv("realistic_restaurant_reviews.csv")  # Load restaurant reviews from CSV file

# Initialize embeddings with explicit host configuration
embeddings = OllamaEmbeddings(
    model="mxbai-embed-large",                 # Specify the embedding model
    base_url="http://localhost:11434"          # Set the Ollama server URL
)

db_location = "./chrome_langchain_db"          # Directory to persist the vector database
add_documents = not os.path.exists(db_location) # Check if database exists; if not, add documents

if add_documents:
    documents = []                             # List to hold Document objects
    ids = []                                   # List to hold document IDs
    
    for i, row in df.iterrows():               # Iterate over each row in the DataFrame
        document = Document(
            page_content=row["Title"] + " " + row["Review"],  # Combine title and review as content
            metadata={"rating": row["Rating"], "date": row["Date"]}, # Store rating and date as metadata
            id=str(i)                                         # Use row index as document ID
        )
        ids.append(str(i))                    # Add ID to list
        documents.append(document)            # Add Document to list
        
vector_store = Chroma(
    collection_name="restaurant_reviews",      # Name of the collection in the vector store
    persist_directory=db_location,             # Directory to persist the vector store
    embedding_function=embeddings              # Embedding function to use
)

if add_documents:
    vector_store.add_documents(documents=documents, ids=ids)  # Add documents to the vector store
    
retriever = vector_store.as_retriever(
    search_kwargs={"k": 5}                     # Configure retriever to return top 5 results
)