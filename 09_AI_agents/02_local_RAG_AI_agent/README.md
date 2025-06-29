# Local RAG AI Agent

A Retrieval-Augmented Generation (RAG) system that uses local LLMs and vector embeddings to answer questions about pizza restaurant reviews. This project demonstrates how to build a conversational AI agent that can retrieve relevant information from a document collection and provide contextual answers.

## Features

- 🤖 **Local LLM Integration**: Uses Ollama with Llama 3.2 model for text generation
- 🔍 **Vector Search**: Implements ChromaDB for efficient similarity search
- 📊 **Document Processing**: Processes restaurant reviews from CSV data
- 💬 **Interactive Chat**: Command-line interface for asking questions
- 🍕 **Domain-Specific**: Specialized for pizza restaurant review analysis

## Architecture

The system consists of three main components:

1. **Vector Store (`vector.py`)**: 
   - Loads restaurant reviews from CSV
   - Creates embeddings using Ollama's mxbai-embed-large model
   - Stores vectors in ChromaDB for fast retrieval

2. **Main Application (`main.py`)**:
   - Implements the chat interface
   - Combines retrieved reviews with user questions
   - Generates responses using Llama 3.2

3. **Data**: CSV file containing realistic pizza restaurant reviews with ratings and dates or you can also add any csv file with reviews.

## Prerequisites

- Python 3.8+
- Ollama installed locally
- Required Ollama models:
  - `llama3.2` (for text generation)
  - `mxbai-embed-large` (for embeddings)

## Installation

1. **Install Python dependencies**:
Create a conda environment:
```bash
conda create -n local_rag_ai_agent python=3.11 -y
conda activate local_rag_ai_agent

```
   ```bash
   pip install -r requirements.txt
   ```

2. **Install and setup Ollama**:
   ```bash
   # Install Ollama (visit https://ollama.ai for platform-specific instructions)
   
   # Pull required models
   ollama pull llama3.2
   ollama pull mxbai-embed-large
   ```

## Usage

1. **Initialize the vector database** (first run only):
   ```bash
   python vector.py
   ```
   This will create the `chrome_langchain_db` directory with embedded reviews.

2. **Start the chat interface**:
   ```bash
   python main.py
   ```

3. **Ask questions about the restaurant**:
   ```
   Ask your question (q to quit): What do customers say about the pizza crust?
   Ask your question (q to quit): Which pizzas have the best ratings?
   Ask your question (q to quit): Are there any gluten-free options?
   Ask your question (q to quit): q
   ```

## Example Queries

- "What do customers say about the pizza crust?"
- "Are there any complaints about delivery?"
- "What are the most popular toppings?"
- "Which reviews mention gluten-free options?"
- "What do customers think about the pricing?"

## Project Structure

```
02_local_RAG_AI_agent/
├── main.py                           # Main chat application
├── vector.py                         # Vector store setup and retrieval
├── realistic_restaurant_reviews.csv  # Sample restaurant review data
├── requirements.txt                  # Python dependencies
├── README.md                         # This file
└── chrome_langchain_db/              # ChromaDB storage (created on first run)
```

## Dependencies

- **langchain**: Core framework for building LLM applications
- **langchain-ollama**: Ollama integration for LangChain
- **langchain-chroma**: ChromaDB vector store integration
- **pandas**: Data manipulation and CSV processing

## How It Works

1. **Data Loading**: Restaurant reviews are loaded from the CSV file containing titles, dates, ratings, and review text.

2. **Document Embedding**: Each review is converted into a vector embedding using the mxbai-embed-large model via Ollama.

3. **Vector Storage**: Embeddings are stored in ChromaDB for efficient similarity search.

4. **Query Processing**: When a user asks a question:
   - The question is embedded using the same model
   - Top 5 most similar reviews are retrieved
   - Retrieved reviews are combined with the question in a prompt template

5. **Response Generation**: The Llama 3.2 model generates a contextual response based on the retrieved reviews and the user's question.

## Customization

### Adding New Data
Replace `realistic_restaurant_reviews.csv` with your own data. Ensure it has columns:
- `Title`: Review title
- `Date`: Review date
- `Rating`: Numeric rating
- `Review`: Review text content

### Changing Models
Modify the model names in:
- `main.py`: Change `OllamaLLM(model="llama3.2")` to your preferred model
- `vector.py`: Change `OllamaEmbeddings(model="mxbai-embed-large")` to your preferred embedding model

### Adjusting Retrieval
In `vector.py`, modify the retriever parameters:
```python
retriever = vector_store.as_retriever(
    search_kwargs={"k": 10}  # Retrieve more documents
)
```

## Troubleshooting

1. **Ollama Connection Issues**: Ensure Ollama is running (`ollama serve`)
2. **Model Not Found**: Pull the required models using `ollama pull <model-name>`
3. **Memory Issues**: Consider using smaller models or reducing the number of retrieved documents
4. **Database Issues**: Delete the `chrome_langchain_db` directory to rebuild the vector store

## Future Enhancements

- Web interface using Streamlit or FastAPI
- Support for multiple data sources
- Advanced filtering and search options
- Chat history and conversation memory
- Performance metrics and evaluation

## License

This project is for educational purposes and demonstrates RAG implementation with local LLMs.


# Tasks for Students
1.  Build an app where you can use this method to genrate RAG based questions and answers for any kinds of document:
   - CSV
   - PDF
   - Word
   - Text
2.  Build a web app using Streamlit or FastAPI to interact with the RAG.