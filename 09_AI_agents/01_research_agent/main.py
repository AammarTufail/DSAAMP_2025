# Import the load_dotenv function to load environment variables from a .env file
from dotenv import load_dotenv
# Import BaseModel from pydantic for data validation and parsing
from pydantic import BaseModel
# Import ChatOpenAI for using OpenAI's chat models
from langchain_openai import ChatOpenAI
# Import ChatAnthropic for using Anthropic's chat models (commented out below)
from langchain_anthropic import ChatAnthropic
# Import os for environment variable manipulation
import os
# Import ssl for SSL configuration
import ssl
# Import httpx for HTTP client configuration
import httpx
# Import ChatPromptTemplate to create structured prompts for the LLM
from langchain_core.prompts import ChatPromptTemplate
# Import PydanticOutputParser to parse LLM outputs into Pydantic models
from langchain_core.output_parsers import PydanticOutputParser
# Import functions to create an agent and execute it
from langchain.agents import create_tool_calling_agent, AgentExecutor
# Import custom tools for the agent to use
from tools import search_tool, wiki_tool, save_tool
# Import datetime for generating timestamps
from datetime import datetime

# Load environment variables from a .env file (e.g., API keys)
load_dotenv()

# Fix SSL certificate issue by removing problematic SSL_CERT_FILE if it exists
if 'SSL_CERT_FILE' in os.environ and not os.path.exists(os.environ['SSL_CERT_FILE']):
    del os.environ['SSL_CERT_FILE']

# Create a custom httpx client that bypasses SSL verification
custom_client = httpx.Client(verify=False)

# Function to save research response to a text file
def save_research_to_file(research_response, query, filename=None):
    """
    Save research response to a text file with timestamp
    """
    if filename is None:
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f"research_output_{timestamp}.txt"
    
    filepath = os.path.join(os.getcwd(), filename)
    
    with open(filepath, 'w', encoding='utf-8') as f:
        f.write(f"Research Query: {query}\n")
        f.write(f"Generated on: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
        f.write("="*50 + "\n\n")
        f.write(f"Topic: {research_response.topic}\n\n")
        f.write(f"Summary:\n{research_response.summary}\n\n")
        f.write(f"Sources Used:\n")
        for i, source in enumerate(research_response.sources, 1):
            f.write(f"{i}. {source}\n")
        f.write(f"\nTools Used: {', '.join(research_response.tools_used)}\n")
    
    return filepath

# Define a Pydantic model for the expected research response structure
class ResearchResponse(BaseModel):
    topic: str                # The research topic
    summary: str              # A summary of the research
    sources: list[str]        # List of sources used
    tools_used: list[str]     # List of tools used

# Initialize the OpenAI chat model (gpt-4o-mini) with custom SSL configuration
llm = ChatOpenAI(
    model="gpt-4o-mini",
    http_client=custom_client
)
# Alternative: Uncomment to use Anthropic's Claude model instead
# llm = ChatAnthropic(model="claude-3-5-sonnet-20241022")

# Create a parser to convert LLM output into the ResearchResponse model
parser = PydanticOutputParser(pydantic_object=ResearchResponse)

# Define the prompt template for the agent, including system instructions and placeholders
prompt = ChatPromptTemplate.from_messages(
    [
        (
            "system",
            """
            You are a research assistant that will help generate a research paper.
            Answer the user query using the available tools efficiently. 
            Use Wikipedia tool for general information and search tool for additional details.
            Once you have gathered sufficient information, provide the final answer in the specified JSON format.
            
            Be concise and focused in your research to avoid exceeding iteration limits.
            
            Wrap the final output in this format and provide no other text:
            {format_instructions}
            """,
        ),
        ("placeholder", "{chat_history}"),      # Placeholder for chat history
        ("human", "{query}"),                   # Placeholder for the user's query
        ("placeholder", "{agent_scratchpad}"),  # Placeholder for agent's scratchpad (internal reasoning)
    ]
# Insert format instructions from the parser into the prompt
).partial(format_instructions=parser.get_format_instructions())

# List of tools the agent can use during research
tools = [search_tool, wiki_tool, save_tool]

# Create the agent with the LLM, prompt, and tools
agent = create_tool_calling_agent(
    llm=llm,
    prompt=prompt,
    tools=tools
)

# Create an executor to run the agent with the specified tools and verbose output
agent_executor = AgentExecutor(
    agent=agent, 
    tools=tools, 
    verbose=True,
    max_iterations=20,  # Increase max iterations to allow more research steps
    handle_parsing_errors=True,  # Handle parsing errors gracefully
    early_stopping_method="generate"  # Allow agent to generate final answer when reaching max iterations
)

# Prompt the user for a research query
query = input("What can i help you in research? ")

# Invoke the agent executor with the user's query and get the raw response
raw_response = agent_executor.invoke({"query": query})

try:
    # Try to parse the agent's output into the structured ResearchResponse model
    # The output is a string containing JSON, so parse it directly
    structured_response = parser.parse(raw_response.get("output"))
    # Print the structured response
    print(structured_response)
    
    # Save the research response to a text file
    saved_file = save_research_to_file(structured_response, query)
    print(f"\nResearch saved to: {saved_file}")
    
except Exception as e:
    # If parsing fails, print an error message and the raw response
    print("Error parsing response", e, "Raw Response - ", raw_response)