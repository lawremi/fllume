import sys
print(f"sys.path inside test: {sys.path}")
import fllume

def test_agent_builder_creates_agent_with_correct_model():
    model_id = "test_provider/test_model"
    agent = fllume.Agent.builder().with_model(model_id).build()
    assert isinstance(agent, fllume.Agent)
    assert agent.model == model_id
