# Building and Understanding AI Agents (with Python)

## Learning goals
1. **Conceptual** – Define *intelligent / autonomous agents* and recognise the major agent architectures.  
2. **Practical** – Create three working agents in Python:  
   * a reflex (rule-based) agent,  
   * an LLM-powered tool-using agent with LangChain,  
   * a small multi-agent team with CrewAI.  
3. **Critical thinking** – Know where agents shine, where they fail, and which frameworks to explore next.

---

## 1.  What is an AI agent?

> *An intelligent agent is an entity that perceives its environment, takes actions autonomously to achieve goals, and can improve its performance over time.*
> AI Agents are a core concept in AI, robotics, and software engineering. They can be simple rule-based systems or complex multi-agent teams.

AI textbooks treat **AI itself as “the study of intelligent agents.”** The key ingredients are:

| Ingredient | Role | Example in code |
|------------|------|-----------------|
| **Percepts** | Raw input from sensors or an API | current room is “dirty” |
| **Internal state / memory** | Helps deal with partial observability | map of explored squares |
| **Policy / reasoning** | Mapping percept → action | `if status=="dirty": return "suck (vacuum cleaner)"` |
| **Actuators / tools** | How the agent changes the world | web-search tool, robot motor |
| **Goals / utility** | What counts as success | vacuumed room, finished report |

---
---

### Environment dimensions of intelligent agents (AI Agents)
| Dimension | Description | Example |
|-----------|-------------|---------|
| **Observable vs. partially observable** | Whether the agent can see the complete state of the environment | Chess board (observable) vs. poker hand (partially observable) |
| **Single-agent vs. multi-agent** | Whether one agent or multiple agents operate in the environment | Solo game vs. multiplayer online game |
| **Deterministic vs. stochastic** | Whether actions have predictable outcomes or involve randomness | Calculator (deterministic) vs. weather prediction (stochastic) |
| **Static vs. dynamic** | Whether the environment changes while the agent is deliberating | Crossword puzzle (static) vs. stock trading (dynamic) |
| **Discrete vs. continuous** | Whether states and actions are countable or form a continuous space | Grid world (discrete) vs. robot navigation (continuous) | 

These dimensions affect how complicated the agent must be.

---

## 2  Agent design patterns

| Family | Main idea | Fits when… | Traditional example |
|--------|-----------|-----------|-------------------|
| **Reflex / rule-based** | Hard-coded *condition → action* rules | small, fully observable tasks | Thermostat (if temp > 36°C → turn on AC) |
| **Model-based** | Keeps an internal model of world state | sensors are noisy, world changes | Robot with SLAM (mapping unknown terrain) |
| **Goal–based / planning** | Searches for a sequence of actions that achieves a goal | long-horizon problems | GPS navigation (finding shortest route) |
| **Utility-based** | Maximises a continuous utility function | trade-offs or risk involved | Investment portfolio optimizer |
| **Learning agents** | Improve the policy with data (e.g. RL) | dynamics unknown or too complex | Game-playing AI (AlphaGo, chess engines) |
| **LLM agents (tool-calling)** | Use a language model to decide **which** tool to call next | open-ended, text-rich tasks | ChatGPT with plugins (web search, calculator) |
| **Multi-agent systems** | Several specialised agents cooperate | complex workflows, parallelism | Air traffic control system |

---

## 3  Hands-on: three agents in Python

### 3.1  Reflex Vacuum-Cleaner agent (no external libraries)

```python
"""vacuum_agent.py – run with Python ≥3.8"""
from random import choice

# Environment -------------------------------------------------
class TwoRoomEnvironment:
    def __init__(self):
        self.state = {"A": choice(["clean", "dirty"]),
                      "B": choice(["clean", "dirty"])}
        self.location = "A"                    # start position

    def percept(self):
        return self.location, self.state[self.location]

    def execute(self, action):
        if action == "suck":
            self.state[self.location] = "clean"
        elif action == "right":
            self.location = "B"
        elif action == "left":
            self.location = "A"

    def is_done(self):
        return all(v == "clean" for v in self.state.values())

# Agent -------------------------------------------------------
class VacuumAgent:
    """Simple reflex agent"""
    def act(self, percept):
        location, status = percept
        if status == "dirty":
            return "suck"
        return "right" if location == "A" else "left"

# Simulation --------------------------------------------------
env, agent, steps = TwoRoomEnvironment(), VacuumAgent(), 0
while not env.is_done() and steps < 10:
    action = agent.act(env.percept())
    env.execute(action)
    steps += 1
print(f"Done in {steps} steps → {env.state}")
```

*Try modifying the rules to see how behaviour changes.*

---

### 3.2  Tool-using LLM agent with **LangChain** (v0.3+)

LangChain offers a helper that wires together:

* a chat-model,
* a list of *tools* (Python callables),
* short-term memory.

```python
# pip install "langchain-core>=0.3" langchain-anthropic langchain-community
from langchain_anthropic import ChatAnthropic
from langchain_community.tools.tavily_search import TavilySearchResults
from langgraph.checkpoint.memory import MemorySaver
from langgraph.prebuilt import create_react_agent

model   = ChatAnthropic(model_name="claude-3-sonnet-20240229")
search  = TavilySearchResults(max_results=2)
memory  = MemorySaver()

agent = create_react_agent(model, tools=[search], checkpointer=memory)

# Stream the reasoning steps
config = {"configurable": {"thread_id": "demo"}}
for step in agent.stream({"messages": ["What is the tallest mountain in Pakistan?"]},
                         config, stream_mode="values"):
    print(step["messages"][-1].content)
```

The language model decides *when* to call the search-tool and integrates results before answering.

---

### 3.3  A cooperative two-agent **CrewAI** team

CrewAI (released 12 June 2025) focuses on role-playing multi-agent “crews.” It is lightweight and doesn’t depend on LangChain citeturn1view0.

```python
# pip install crewai
from crewai import Agent, Task, Crew, Process

# 1️⃣ Define specialist agents
researcher = Agent(
    role="Researcher",
    goal="Find the official Python 3.13 release date",
    backstory="You scour official sources and PEPs with precision."
)
writer = Agent(
    role="Writer",
    goal="Turn research into a concise paragraph",
    backstory="You craft clear technical prose."
)

# 2️⃣ Define tasks
t_research = Task(
    description="Look up the scheduled release date of Python 3.13.",
    expected_output="A date in ISO format (YYYY-MM-DD).",
    agent=researcher
)
t_write = Task(
    description="Create a 100-word summary mentioning the date.",
    expected_output="Markdown paragraph.",
    agent=writer
)

# 3️⃣ Assemble and run the crew
crew = Crew(
    agents=[researcher, writer],
    tasks=[t_research, t_write],
    process=Process.sequential,
    verbose=True
)
crew.kickoff()
```

> Under the hood, each agent prompts its underlying LLM; CrewAI routes intermediate outputs between agents and gives you optional observability hooks.

---

## 4  Choosing a framework in 2025

| Framework | Strengths | When to pick it |
|-----------|-----------|-----------------|
| **LangChain / LangGraph** | Mature ecosystem, great for **single LLM agents** with many tools, integrates vector stores | Retrieval-augmented chat-bots, function-calling |
| **CrewAI** (0.13+) | Lean, role-based **multi-agent** orchestration; YAML project scaffolding; easy to mix “Crews” and **Flows** for more deterministic control | Workflow automation, content pipelines |
| **Microsoft AutoGen 0.4** | Asynchronous, event-driven architecture, strong observability, cross-language (.NET) support  | Large-scale, long-running enterprise agents |
| **Google ADK (Agent Development Kit)** | Open-source, modular toolkit for building, evaluating, and deploying LLM-powered agents; strong focus on reproducibility and benchmarking | Research, rapid prototyping, and standardized agent evaluation |


---

## 5  Best practices & pitfalls

* **Tool safety** – Whitelist actions an agent may take; validate outputs.  
* **Memory scope** – Short-term conversation memory ≠ long-term ground-truth store.  
* **Evaluation** – Record traces and define *task-level* success metrics, not just token accuracy.  
* **Budgeting** – Keep a cost/latency log; agents that decide poorly can loop.  
* **Human-in-the-loop** – Add override checkpoints for critical tasks (e.g. purchases).

---

## 6 Applications of AI Agents


AI Agents are powering the next wave of billion-dollar startups. Here are high-impact applications where intelligent agents create massive value:

### 6.1 Business Process Automation
* **AI Executive Assistant** - Multi-agent teams that manage calendars, emails, meeting prep, and follow-ups across entire organizations
* **Contract Intelligence** - Agents that read, negotiate, and draft legal documents with human oversight
* **Financial Planning Bots** - Personal CFO agents that optimize spending, investments, and tax strategies for individuals and SMBs

### 6.2 Content & Creative Industries  
* **Personalized Education** - Adaptive tutoring agents that create custom curricula and adjust teaching styles per student
* **Social Media Management** - Multi-platform agents that create, schedule, and optimize content while engaging with audiences
* **Video Game NPCs** - LLM-powered characters that provide truly dynamic, contextual interactions in gaming environments

### 6.3 Healthcare & Wellness
* **Medical Triage Agents** - First-line diagnostic assistants that route patients to appropriate specialists based on symptoms
* **Mental Health Companions** - Always-available therapy-trained agents providing CBT and emotional support
* **Drug Discovery Acceleration** - Research agents that analyze scientific literature and propose novel compound combinations

### 6.4 Sales & Customer Success
* **Hyper-Personalized Outreach** - Sales agents that research prospects, craft custom messages, and handle initial conversations
* **Customer Success Automation** - Agents that proactively identify churn risk and execute retention campaigns
* **E-commerce Personal Shoppers** - Shopping assistants that understand style preferences and budget constraints

### 6.5 Emerging Opportunities
* **Smart Home Orchestration** - Agents that learn family patterns and optimize energy, security, and comfort automatically  
* **Supply Chain Intelligence** - Multi-agent systems that predict disruptions and automatically reroute logistics
* **Code Generation & Debugging** - Full-stack development agents that can build, test, and deploy applications end-to-end

**💡 Startup Success Formula**: Pick a $10B+ industry with manual, repetitive workflows → Build specialized agent teams → Focus on measurable ROI → Scale through API partnerships.



---

## 7  Further reading

1. [Wikipedia overview of intelligent agents ](https://en.wikipedia.org/wiki/Intelligent_agent?utm_source=chatgpt.com) 
2. [LangChain *Build an Agent* tutorial (2025-03)](https://python.langchain.com/docs/tutorials/agents/) 
3. [CrewAI PyPI page & docs (v0.13, 2025-06-12)](https://pypi.org/project/crewai/)  
4. [Microsoft Research blog on AutoGen 0.4 (2025-01-14) ](https://www.microsoft.com/en-us/research/blog/autogen-v0-4-reimagining-the-foundation-of-agentic-ai-for-scale-extensibility-and-robustness/)


