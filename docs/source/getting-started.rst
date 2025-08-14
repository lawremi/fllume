Getting Started
===============

This guide will walk you through installing fllume and building your first agent, step-by-step.

Installation
------------

First, you need to install fllume. We recommend using `uv`. You can find detailed instructions in the main `README.md <https://github.com/lawremi/fllume/blob/main/README.md>`_ on GitHub.

Prerequisites
-------------

The examples in this guide use the OpenAI API. Before you begin, make sure you have set your OpenAI API key as an environment variable:

.. code-block:: bash

   export OPENAI_API_KEY="your-api-key-here"

Your First Completion
---------------------

Let's start with the simplest possible agent. We'll create an agent that uses ``openai/gpt-4o-mini`` and ask it a simple question.

.. code-block:: python

   from fllume.agent import Agent

   # Create a simple agent
   agent = Agent.builder().with_model("openai/gpt-4o-mini").build()

   # Get a response
   response = agent.complete("What is the capital of France?")
   print(response)

This demonstrates the core functionality: building an agent and getting a completion.

Adding Structure with ``response_format``
-----------------------------------------

Often, you need a response in a specific, predictable format. `fllume` makes this easy by integrating with Pydantic models.

Let's create an agent that extracts structured data from a sentence.

.. code-block:: python

   from fllume.agent import Agent
   from pydantic import BaseModel

   class User(BaseModel):
       name: str
       age: int

   # Create an agent that returns a User object
   structured_agent = (
       Agent.builder()
       .with_model("openai/gpt-4o-mini")
       .with_response_format(User)
       .build()
   )

   response = structured_agent.complete(
       "The user's name is Jean-Luc and he is 59 years old."
   )

   print(response)
   # Expected output: name='Jean-Luc' age=59
   print(f"User's age: {response.age}")

Adding Capabilities with Tools
------------------------------

You can give your agent new abilities by providing it with Python functions as tools. `fllume` handles the complex parts of making the LLM aware of the tools and executing them. This is ideal for data science tasks like performing custom calculations.

.. code-block:: python

   from fllume.agent import Agent

   def calculate_average(numbers: list[float]) -> float:
       """Calculates the average of a list of numbers."""
       return sum(numbers) / len(numbers)

   tool_agent = (
       Agent.builder()
       .with_model("openai/gpt-4o-mini")
       .with_tools([calculate_average])
       .build()
   )

   data = [10.5, 20.3, 15.7, 25.1, 12.9]
   response = tool_agent.complete(f"What is the average of these numbers: {data}?")
   print(response)
   # Expected output: The average of the numbers is 16.9.

Streaming Responses
-------------------

For long-form content like reports or summaries, you can stream the response word by word. This provides a much better user experience.

.. code-block:: python

   import pandas as pd
   from fllume.agent import Agent

   # Sample data for demonstration
   data = {
       'City': ['New York', 'Los Angeles', 'Chicago'],
       'Population': [8419000, 3980000, 2716000]
   }
   df = pd.DataFrame(data)

   streaming_agent = (
       Agent.builder()
       .with_model("openai/gpt-4o-mini")
       .with_instructions("You are a data analyst.")
       .build()
   )

   prompt = f"Provide a brief summary of the following dataset:\n{df.to_string()}"
   stream = streaming_agent.complete(prompt, stream=True)

   print("Streaming summary:")
   for chunk in stream:
       print(chunk, end="", flush=True)
   print()

Building Multi-turn Conversations
---------------------------------

For more complex interactions, like iteratively developing an analysis plan or a plotting script, you need to maintain a conversation history. The ``complete_with_context`` method is designed for this. You pass the context from the previous turn to the next one.

.. code-block:: python

   from fllume.agent import Agent

   plotting_assistant = (
       Agent.builder()
       .with_model("openai/gpt-4o-mini")
       .with_instructions(
           "You are a data visualization assistant. You provide Python code "
           "snippets for generating plots with matplotlib."
       )
       .build()
   )

   # First turn: Ask for a basic plot
   context = plotting_assistant.complete_with_context(
       prompt="Give me some code to create a simple scatter plot of x vs y."
   )
   print(f"Assistant: {context[-1]['content']}")

   # Second turn: Ask for a modification
   context = plotting_assistant.complete_with_context(
       context=context,
       prompt="Now, can you modify that to make the points blue and add a title?"
   )
   print(f"\nAssistant: {context[-1]['content']}")

Next Steps
----------

You've now seen the core features of `fllume`. To learn more, check out the following resources:

- :doc:`examples`: More detailed, real-world examples.
- :doc:`api`: The complete API reference for all classes and methods.