import pytest
import os
import fllume
from dotenv import load_dotenv
from typing import Generator
from pydantic import BaseModel

load_dotenv()

requires_openai = pytest.mark.skipif(
    "OPENAI_API_KEY" not in os.environ,
    reason="OPENAI_API_KEY not set in environment",
)

MODEL = "openai/gpt-4o-mini"

@requires_openai
def test_agent_simple_completion():
    agent = (
        fllume.Agent.builder()
        .with_model(MODEL)
        .build()
    )
    prompt = "What is the capital of France?"
    response = agent.complete(prompt)

    assert isinstance(response, str)
    assert "Paris" in response

@requires_openai
def test_agent_streaming_completion():
    agent = (
        fllume.Agent.builder()
        .with_model(MODEL)
        .build()
    )
    prompt = "What is the capital of France?"
    stream = agent.complete(prompt, stream=True)

    assert isinstance(stream, Generator)

    response_parts = []
    for chunk in stream:
        assert isinstance(chunk, str)
        response_parts.append(chunk)

    assert len(response_parts) > 1

    full_response = "".join(response_parts)
    assert "Paris" in full_response
 
def get_user_name(user_id: int) -> str:
    """A dummy tool to get a username from a user ID."""
    if user_id == 123:
        return "Alice"
    return "Unknown User"

@requires_openai
def test_agent_tool_calling():
    agent = (
        fllume.Agent.builder()
        .with_model(MODEL)
        .with_tools([get_user_name])
        .build()
    )
    prompt = "What is the username for user ID 123?"
    response = agent.complete(prompt)

    assert isinstance(response, str)
    assert "Alice" in response


@requires_openai
def test_agent_tool_calling_streaming():
    """
    Tests that the agent can correctly use a provided tool while streaming.
    """
    agent = (
        fllume.Agent.builder()
        .with_model(MODEL)
        .with_tools([get_user_name])
        .build()
    )
    prompt = "What is the username for user ID 123?"
    stream = agent.complete(prompt, stream=True)

    assert isinstance(stream, Generator)

    response_parts = []
    for chunk in stream:
        assert isinstance(chunk, str)
        response_parts.append(chunk)

    full_response = "".join(response_parts)
    assert "Alice" in full_response

class User(BaseModel):
    name: str
    age: int

@requires_openai
def test_agent_response_format():
    agent = (
        fllume.Agent.builder()
        .with_model(MODEL)
        .with_response_format(User)
        .build()
    )
    prompt = "The user's name is Jean-Luc and he is 59 years old."
    response = agent.complete(prompt)

    assert isinstance(response, User)
    assert response.name == "Jean-Luc"
    assert response.age == 59
