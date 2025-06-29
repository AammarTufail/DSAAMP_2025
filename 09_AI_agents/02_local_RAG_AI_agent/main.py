import os
import ssl
import urllib3
import warnings

# Set environment variables to disable SSL verification and telemetry before any other imports
os.environ['PYTHONHTTPSVERIFY'] = '0'  # Disables Python's HTTPS certificate verification
os.environ['CURL_CA_BUNDLE'] = ''      # Unsets CURL CA bundle to avoid SSL errors
os.environ['REQUESTS_CA_BUNDLE'] = ''  # Unsets Requests CA bundle for SSL

# Disable various telemetry and analytics features for LangChain and related libraries
os.environ['LANGCHAIN_TRACING_V2'] = 'false'
os.environ['LANGCHAIN_TELEMETRY'] = 'false'
os.environ['LANGSMITH_TRACING'] = 'false'
os.environ['LANGCHAIN_ANALYTICS'] = 'false'
os.environ['LANGCHAIN_CALLBACKS_MANAGER'] = 'false'
os.environ['LANGCHAIN_VERBOSE'] = 'false'
os.environ['LANGCHAIN_DEBUG'] = 'false'

# Suppress all warnings, including those related to telemetry and SSL
warnings.filterwarnings("ignore")

# Remove SSL_CERT_FILE from environment if it exists, to avoid SSL issues
if 'SSL_CERT_FILE' in os.environ:
    del os.environ['SSL_CERT_FILE']

# Disable SSL warnings from urllib3 (commonly used by requests and other HTTP libraries)
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

# Set the default SSL context to not verify certificates (insecure, but useful for local dev)
ssl._create_default_https_context = ssl._create_unverified_context

# Import Ollama LLM integration and prompt template from LangChain, and a retriever from local vector module
from langchain_ollama.llms import OllamaLLM
from langchain_core.prompts import ChatPromptTemplate
from vector import retriever

# Initialize the Ollama LLM with the model name and explicit base URL for the local Ollama server
model = OllamaLLM(
    model="llama3.2",
    base_url="http://localhost:11434"  # Ollama server endpoint
)

# Define the prompt template for the chatbot, including placeholders for reviews and question
template = """
You are an exeprt in answering questions about a pizza restaurant

Here are some relevant reviews: {reviews}

Here is the question to answer: {question}
"""
prompt = ChatPromptTemplate.from_template(template)

# Create a chain that combines the prompt and the model
chain = prompt | model

# Start an interactive loop to accept user questions
while True:
    print("\n\n-------------------------------")
    question = input("Ask your question (q to quit): ")
    print("\n\n")
    if question == "q":
        break  # Exit the loop if user enters 'q'
    
    # Retrieve relevant reviews using the retriever for the given question
    reviews = retriever.invoke(question)
    # Invoke the chain with the reviews and question, and get the model's answer
    result = chain.invoke({"reviews": reviews, "question": question})
    # Print the result to the user
    print(result)