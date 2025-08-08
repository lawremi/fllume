import any_llm
from typing import Type, Iterator, Union, Generator, Any

class Agent:
    def __init__(self, model: str, context: list[dict[str, Any]]):
        self.model = model
        self.context = context
    
    @classmethod
    def builder(cls) -> 'AgentBuilder':
        return AgentBuilder(cls)

    def _stream_completion(
        self, completions: Iterator[Any]
    ) -> Generator[str, None, None]:
        """
        Helper generator method to process streaming chunks from 
        any_llm.completion().
        """
        for chunk in completions:
            content = chunk.choices[0].delta.content
            if content is not None:
                yield content

    def complete(
        self, prompt: str, stream: bool = False
    ) -> Union[str, Generator[str, None, None]]:
        completion = any_llm.completion(
            self.model, 
            messages = self.context + [{"role": "user", "content": prompt}],
            stream = stream
        )
        if stream:
            return self._stream_completion(completion)
        else:
            return completion.choices[0].message.content
    
    def __repr__(self) -> str:
        return f'Agent(model={self.model}, context={self.context})'

class AgentBuilder:
    def __init__(self, agent_cls: Type[Agent]):
        self.agent_cls = agent_cls
        self.model = None
        self.context = []

    def build(self) -> Agent:
        assert self.model is not None, "Model must be specified"    
        return self.agent_cls(self.model, self.context)

    def with_model(self, model: str) -> 'AgentBuilder':
        self.model = model
        return self
    
    def with_context(self, context: list[dict[str, Any]]):
        self.context = context
        return self