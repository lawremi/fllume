# fllume: A Fluent Python API for LLM Agents

fllume provides a fluent API for data scientists to build and interact with Large Language Model (LLM) agents in Python. Inspired by fluent APIs in the R ecosystem but adapted for Python, fllume simplifies interactions with LLMs by treating them as functions with structured inputs and outputs.

Core features include tool calling, prompt templating, and seamless conversion between JSON and Python objects. It supports local and remote LLMs—including Ollama, llama.cpp, OpenAI, and Azure—through the extensible `any-llm` backend. Experimental support is available for text embedding, vector stores, and Retrieval-Augmented Generation (RAG).

## Optional System Requirements

- Ollama (for local LLM support)
  - Install from [ollama.ai](https://ollama.ai)
  - Follow platform-specific installation instructions on their website

## Installation

### Using uv (recommended)

```bash
# Install directly from GitHub
uv pip install git+https://github.com/lawremi/fllume.git

# Or install in editable mode for development
git clone https://github.com/lawremi/fllume.git
cd fllume
uv pip install -e .
```

### Using pip

```bash
# Install directly from GitHub
pip install git+https://github.com/lawremi/fllume.git

# Or install in editable mode for development
git clone https://github.com/lawremi/fllume.git
cd fllume
pip install -e .
```

## Usage

See the documentation and examples for detailed usage instructions:

```python
# Import the package
import fllume

# View available modules
help(fllume)
```

## Support

- GitHub Issues: [https://github.com/lawremi/fllume/issues](https://github.com/lawremi/fllume/issues)
- Documentation: [https://lawremi.github.io/fllume/](https://lawremi.github.io/fllume/)

## Development

This project is inspired by the R package [wizrd](https://github.com/lawremi/wizrd), adapted to provide a fluent, Python-native experience for working with LLMs.
