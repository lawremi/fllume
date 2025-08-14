# fllume: A Fluent Python API for LLM Agents

fllume (a portmanteau of **flu**ent and **LLM**) provides a fluent API for data scientists to build and interact with Large Language Model (LLM) agents in Python. Inspired by fluent APIs in the R ecosystem but adapted for Python, fllume simplifies interactions with LLMs so that data scientists can more easily apply them to their scientific workflows. For example, an agent could execute a database query, munge data, generate a workflow, or produce a report. The goal is to enable data scientists to experiment with using LLMs in their programmatic workflows, _not_ to provide a chatbot in Python (see e.g. [chatlas](https://github.com/posit-dev/chatlas) for that).

## Installation

To install the latest version for direct use:
```bash
uv pip install git+https://github.com/lawremi/fllume.git
```

### Development Setup

For local development, it is recommended to create and activate a virtual environment.

```bash
# 1. Clone the repository
git clone https://github.com/lawremi/fllume.git
cd fllume

# 2. Create and activate a virtual environment
uv venv
source .venv/bin/activate  # On Windows, use `.venv\Scripts\activate`

# 3. Install in editable mode with all development dependencies
uv pip install -e ".[dev,doc]"
```

## Usage

The `fllume.agent.Agent` class provides a high-level interface for interacting with LLMs, supporting features like instructions, tool use, structured response formats, and streaming. The `AgentBuilder` class offers a fluent API for configuring `Agent` instances. All examples below utilize the `AgentBuilder` for clarity and best practice.

**Note**: The examples below use `openai/gpt-4o-mini`. To run them, ensure you have the `OPENAI_API_KEY` environment variable set. 

The `fllume` library uses [any-llm](https://github.com/mozilla-ai/any-llm) under the hood, so the available model providers will depend on how `any-llm` was installed. See its documentation for more information on installing provider support.

### Example 1: Data Standardization and Extraction

Use an agent to standardize unstructured address data into a structured Pydantic model, ideal for cleaning and preparing datasets.

```python
from fllume.agent import Agent
from pydantic import BaseModel
import pandas as pd

class StandardizedAddress(BaseModel):
    street: str
    city: str
    state: str
    zip_code: str

agent_address_standardizer = (
    Agent.builder()
    .with_model("openai/gpt-4o-mini")
    .with_instructions("Standardize the given address into its components: street, city, state, and zip code.")
    .with_response_format(StandardizedAddress)
    .with_prompt_template("Standardize this address: {address}")
    .build()
)

address_data = [
    "1600 Amphitheatre Parkway, Mountain View, CA 94043",
    "795 Folsom St, San Francisco, CA 94107",
    "1 Infinite Loop, Cupertino, CA 95014"
]

standardized_addresses = [
    agent_address_standardizer.complete({"address": address}).model_dump() 
    for address in address_data
]

df_addresses = pd.DataFrame(standardized_addresses)
print("Standardized Addresses:")
print(df_addresses)
```

### Example 2: Numerical Computation with Tools

Integrate custom Python functions as tools for your agent to perform specific computations or data manipulations. This example also shows how a single agent can be reused for different but related tasks by using a prompt template.

```python
from fllume.agent import Agent

def calculate_average(numbers: list[float]) -> float:
    """Calculates the average of a list of numbers."""
    return sum(numbers) / len(numbers)

def find_max(numbers: list[float]) -> float:
    """Finds the maximum value in a list of numbers."""
    return max(numbers)

agent_data_analyzer = (
    Agent.builder()
    .with_model("openai/gpt-4o-mini")
    .with_instructions("As a data summarizer, output a single number")
    .with_tools([calculate_average, find_max])
    .with_prompt_template("What is the {statistic} of these numbers: {numbers}?")
    .build()
)

data_points = [10.5, 20.3, 15.7, 25.1, 12.9]

response_avg = agent_data_analyzer.complete({"statistic": "average", "numbers": data_points})
print(f"\nAverage: {response_avg}")

response_max = agent_data_analyzer.complete({"statistic": "maximum value", "numbers": data_points})
print(f"Maximum: {response_max}")
```

### Example 3: Generating Data Summaries with Streaming

Use streaming to generate detailed, potentially long, summaries or explanations of complex datasets or analysis results. This is useful for creating dynamic reports or interactive data narratives.

```python
from fllume.agent import Agent
import pandas as pd

# Sample data for demonstration
data = {
    'City': ['New York', 'Los Angeles', 'Chicago', 'Houston', 'Phoenix'],
    'Population': [8419000, 3980000, 2716000, 2320000, 1660000],
    'Area_sq_mi': [302.6, 468.7, 234.0, 637.4, 517.9]
}
df = pd.DataFrame(data)

agent_data_summarizer = (
    Agent.builder()
    .with_model("openai/gpt-4o-mini")
    .with_instructions("You are a data analyst. Summarize the key insights from the provided DataFrame, focusing on population and area trends. Be concise but informative.")
    .with_prompt_template("Summarize the following DataFrame:\n{dataframe}")
    .build()
)

print("\nData Summary (Streaming):")
# Convert DataFrame to string for the LLM to process
df_str = df.to_string()
for chunk in agent_data_summarizer.complete({"dataframe": df_str}, stream=True):
    print(chunk, end="", flush=True)
print()
```

### Example 4: Multi-turn Conversations
fllume can maintain conversational context, allowing for follow-up questions and more complex interactions.
```python
from fllume.agent import Agent
# Create an agent
plotting_assistant = (
    Agent.builder()
    .with_model("openai/gpt-4o-mini")
    .with_instructions(
        "You are a data visualization assistant. You provide Python code "
        "snippets for generating plots with matplotlib."
    )
    .build()
)

# First turn
context = plotting_assistant.complete_with_context(
    prompt="Give me some code to create a simple scatter plot of x vs y.",
)
print(f"Assistant: {context[-1].content}")

# Ask a follow-up question. The agent remembers the previous turn.
context = plotting_assistant.complete_with_context(
    context=context,
    prompt="Now, can you modify that to make the points blue and add a title?",
)
print(f"\nAssistant: {context[-1].content}")
```

## A Lightweight Convenience Layer for LLM Interactions

`fllume` provides a Pythonic, fluent interface that simplifies common LLM interaction patterns, abstracting away much of the boilerplate often found in direct LLM API calls.

`fllume` streamlines these processes by:

- **Fluent API for Agent Configuration**: The `AgentBuilder` provides a readable and chainable interface for configuring complex agents, making your code cleaner and more maintainable.
- **Simplified Tool Integration**: Define your tools as standard Python functions, and `fllume` handles the intricate details of tool call detection, execution, and response injection into the LLM's context.
- **Convenient Structured Output**: Easily enforce structured outputs using Pydantic models, ensuring your LLM responses are consistently formatted and ready for downstream processing.
- **Reusable Prompt Templates**: Define a prompt with placeholders and pass data as a dictionary, simplifying iterative calls and separating logic from data.

This approach significantly reduces the cognitive load and lines of code required to build sophisticated LLM-powered applications, making `fllume` suitable for data scientists and developers looking for a more intuitive way to integrate LLMs into their workflows.

## Support

- GitHub Issues: [https://github.com/lawremi/fllume/issues](https://github.com/lawremi/fllume/issues)
- Documentation: [https://lawremi.github.io/fllume/](https://lawremi.github.io/fllume/)

## Development

This project uses `ruff` for linting and formatting. To check your code locally before committing, you can run:

### Running Tests

The project uses pytest for testing. To run the full test suite:
```bash
uv run pytest
```
Note: Some tests make live API calls and require the `OPENAI_API_KEY` environment variable to be set. These tests will be automatically skipped if the key is not found.

### Linting and formatting

```bash
# Check for linting errors
uv run ruff check .

# Automatically format files
uv run ruff format .
```

### Continuous Integration (CI)

This project uses GitHub Actions to automatically run tests and linting on every
push and pull request to the main branch. The CI pipeline will fail if:
- The tests do not pass.
- The linting checks fail.
- The code is not formatted correctly according to ruff.

Before pushing your changes, it is recommended to run `uv run pytest` , `uv run ruff check` 
and `uv run ruff format` and locally to ensure the CI checks will pass.

## Background

This project is inspired by the R package [wizrd](https://github.com/lawremi/wizrd), adapted to provide a fluent, Python-native experience for working with LLMs.
