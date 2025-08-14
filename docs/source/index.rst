fllume Documentation
====================

Welcome to **fllume**, a fluent Python API for data scientists to build and interact with Large Language Model (LLM) agents.

.. image:: https://img.shields.io/pypi/v/fllume.svg
   :target: https://pypi.org/project/fllume/
   :alt: PyPI version

.. image:: https://img.shields.io/pypi/pyversions/fllume.svg
   :target: https://pypi.org/project/fllume/
   :alt: Python versions

.. image:: https://img.shields.io/github/license/lawremi/fllume.svg
   :target: https://github.com/lawremi/fllume/blob/main/LICENSE
   :alt: License

What is fllume?
---------------

fllume provides a clean, intuitive API for building LLM-powered agents that can:

* **Execute complex workflows** with tool integration
* **Generate structured responses** using Pydantic models
* **Handle multi-turn conversations** with context management
* **Stream responses** for real-time applications

The library is built on top of the `any-llm <https://mozilla-ai.github.io/any-llm/>`_ SDK, providing access to multiple LLM providers through a unified interface.

Key Features
------------

🔗 **Fluent API Design**
   Chain methods naturally with an intuitive builder pattern designed for data science workflows.

🛠️ **Easy Tool Integration**
   Convert Python functions into LLM tools with automatic schema generation and error handling.

📊 **Structured Output**
   Get consistent, typed responses using Pydantic models for reliable data processing.

🔄 **Multi-turn Conversations**
   Maintain conversation context across multiple interactions for complex workflows.

⚡ **Streaming Support**
   Stream responses in real-time for interactive applications and long-running tasks.

🌐 **Multiple LLM Providers**
   Support for OpenAI, Anthropic, Ollama, and other providers through any-llm integration.

Quick Start
-----------

Install fllume using your preferred package manager:

.. code-block:: bash

   # Using uv (recommended)
   uv add fllume
   
   # Using pip
   pip install fllume

Create your first agent:

.. code-block:: python

   from fllume import Agent
   
   # Create an agent with the fluent API
   agent = (Agent.builder()
       .with_model("openai/gpt-4")
       .with_instructions("You are a helpful data science assistant")
       .build())
   
   # Get a response
   response = agent.complete("Explain linear regression in simple terms")
   print(response)

Example with Tools
------------------

Here's a more advanced example showing tool integration:

.. code-block:: python

   from fllume import Agent
   from pydantic import BaseModel
   import pandas as pd
   
   def analyze_data(csv_path: str) -> str:
       """Analyze a CSV file and return basic statistics."""
       df = pd.read_csv(csv_path)
       return f"Shape: {df.shape}, Columns: {list(df.columns)}"
   
   class AnalysisResult(BaseModel):
       summary: str
       recommendations: list[str]
       confidence: float
   
   # Create an agent with tools and structured output
   analyst = (Agent.builder()
       .with_model("openai/gpt-4")
       .with_instructions("You are a data analyst assistant")
       .with_tools([analyze_data])
       .with_response_format(AnalysisResult)
       .build())
   
   # Get structured analysis
   result = analyst.complete("Help me get started with data.csv")
   print(f"Summary: {result.summary}")
   print(f"Recommendations: {result.recommendations}")
   print(f"Confidence: {result.confidence}")

Documentation Contents
----------------------

.. toctree::
   :maxdepth: 2
   :caption: User Guide

   getting-started
   api

.. toctree::
   :maxdepth: 1
   :caption: API Reference

   api

Indices and tables
==================

* :ref:`genindex`
* :ref:`modindex`
* :ref:`search`

Getting Help
============

If you encounter any issues or have questions:

* Check the :doc:`getting-started` guide for common setup issues and usage patterns
* Visit the `GitHub repository <https://github.com/lawremi/fllume>`_ to report bugs or request features
* Review the `issue tracker <https://github.com/lawremi/fllume/issues>`_ for known issues

Contributing
============

fllume is an open-source project and contributions are welcome! Please see the 
`contributing guidelines <https://github.com/lawremi/fllume/blob/main/CONTRIBUTING.md>`_ 
for more information.

License
=======

fllume is released under the MIT License. See the 
`LICENSE file <https://github.com/lawremi/fllume/blob/main/LICENSE>`_ for details.