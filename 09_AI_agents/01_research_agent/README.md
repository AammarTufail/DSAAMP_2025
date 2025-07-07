# Python AI Research Agent

## Overview

This project provides a command-line AI agent designed to assist with research tasks. The agent leverages large language models (LLMs) and custom tools to answer queries, summarize information, and provide structured research insights. It supports both OpenAI and Anthropic models, and uses Pydantic for robust output parsing.

## Features

- Query knowledge bases using natural language.
- Summarize and structure research results.
- Cite sources and list tools used for transparency.
- Command-line interface for easy interaction.
- Supports multiple LLM providers (OpenAI, Anthropic).
- Extensible with custom research tools.
- Graceful error handling and output validation.

## How It Works

1. **Environment Setup**: Loads API keys and environment variables from a `.env` file.
2. **Model Selection**: Uses OpenAI's GPT-4o-mini by default (switchable to Anthropic's Claude).
3. **Prompt Engineering**: Crafts a structured prompt for the LLM, instructing it to use tools and return output in a specific format.
4. **Tool Integration**: Integrates custom tools (search, wiki, save) for enhanced research capabilities.
5. **Output Parsing**: Uses Pydantic to validate and parse the LLM's response into a structured format.
6. **User Interaction**: Prompts the user for a research query and displays structured results.

## Example Usage

```bash
$ python research_agent.py
What can I help you research? Quantum computing applications in medicine
```

Example output:
```json
{
    "topic": "Quantum computing applications in medicine",
    "summary": "Quantum computing is being explored for drug discovery, genomics, and medical imaging. It offers potential speedups for complex simulations and data analysis.",
    "sources": [
        "https://www.nature.com/articles/s41586-019-1666-5",
        "https://www.ibm.com/blog/quantum-computing-healthcare/"
    ],
    "tools_used": [
        "search_tool",
        "wiki_tool"
    ]
}
```

## Requirements

- Python 3.10+
- `langchain`, `langchain_openai`, `langchain_anthropic`
- `pydantic`
- `python-dotenv`
- API keys for OpenAI and/or Anthropic (in `.env`)

## Setup

1. Clone the repository.
2. Install dependencies:
     ```bash
     pip install -r requirements.txt
     ```
3. Create a `.env` file with your API keys:
     ```
     OPENAI_API_KEY=your_openai_key
     ANTHROPIC_API_KEY=your_anthropic_key
     ```
4. Run the agent:
     ```bash
     python main.py
     ```

## Customization

- Add or modify tools in `tools.py` to extend agent capabilities.
- Switch LLM providers by commenting/uncommenting the relevant lines in the code.

## License

This project is licensed under the MIT License.
