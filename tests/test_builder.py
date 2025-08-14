import pytest
import fllume
from pydantic import BaseModel


def test_agent_builder_fails_if_not_given_model():
    """Tests that the builder raises an AssertionError if no model is provided."""
    with pytest.raises(AssertionError, match="Model must be specified"):
        fllume.Agent.builder().build()


def test_agent_builder_with_model():
    model_id = "test_provider/test_model"
    agent = fllume.Agent.builder().with_model(model_id).build()
    assert isinstance(agent, fllume.Agent)
    assert agent.model == model_id


def test_agent_builder_with_instructions():
    model_id = "test_provider/test_model"
    instructions = "You are a test assistant."
    agent = (
        fllume.Agent.builder()
        .with_model(model_id)
        .with_instructions(instructions)
        .build()
    )
    assert agent.instructions == instructions


def to_uppercase(text: str) -> str:
    """Converts input text to uppercase."""
    return text.upper()


def test_agent_builder_with_tools():
    model_id = "test_provider/test_model"
    tools = [to_uppercase]
    agent = fllume.Agent.builder().with_model(model_id).with_tools(tools).build()
    assert isinstance(agent, fllume.Agent)
    assert agent.tools == tools


class DummyModel(BaseModel):
    """A dummy Pydantic model for testing."""

    field: str


def test_agent_builder_with_response_format():
    model_id = "test_provider/test_model"
    agent = (
        fllume.Agent.builder()
        .with_model(model_id)
        .with_response_format(DummyModel)
        .build()
    )
    assert agent.response_format == DummyModel


def test_agent_builder_with_prompt_template():
    model_id = "test_provider/test_model"
    template = "This is a {variable}."
    agent = (
        fllume.Agent.builder()
        .with_model(model_id)
        .with_prompt_template(template)
        .build()
    )
    assert agent.prompt_template == template


def test_agent_builder_with_params():
    model_id = "test_provider/test_model"
    params = {"temperature": 0.5}
    agent = fllume.Agent.builder().with_model(model_id).with_params(params).build()
    assert isinstance(agent, fllume.Agent)
    assert agent.params == params
