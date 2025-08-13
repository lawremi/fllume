import sys
import fllume

def test_agent_builder_creates_agent_with_correct_model():
    model_id = "test_provider/test_model"
    agent = fllume.Agent.builder().with_model(model_id).build()
    assert isinstance(agent, fllume.Agent)
    assert agent.model == model_id

def test_agent_builder_fails_if_not_given_model():
    try:
        fllume.Agent.builder().build()
        assert False
    except:
        assert True

def test_agent_builder_creates_agent_with_correct_params():
    model_id = "test_provider/test_model"
    params = {"temperature": 0.5}
    agent = (
        fllume.Agent.builder().
        with_model(model_id).
        with_params(params).
        build()
    )
    assert isinstance(agent, fllume.Agent)
    assert agent.params == params

def to_uppercase(text: str) -> str:
    """Converts input text to uppercase."""
    return text.upper()

def test_agent_builder_creates_agent_with_correct_tools():
    model_id = "test_provider/test_model"
    tools = [to_uppercase]
    agent = (
        fllume.Agent.builder().
        with_model(model_id).
        with_tools(tools).
        build()
    )
    assert isinstance(agent, fllume.Agent)
    assert agent.tools == tools
