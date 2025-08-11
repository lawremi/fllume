import any_llm
from typing import Type, Iterator, Union, Generator, Any

class Agent:
    def __init__(
        self, 
        model: str, 
        context: list[dict[str, Any]], 
        instructions: str, 
        params: dict[str, Any]
    ):
        self.model = model
        self.context = context
        self.instructions = instructions
        self.params = params
    
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
            messages = (
                self.context
                + (
                    [{"role": "system", "content": self.instructions}] 
                    if self.instructions else []
                )
                + [{"role": "user", "content": prompt}]
            ),
            stream = stream,
            **self.params
        )
        if stream:
            return self._stream_completion(completion)
        else:
            return completion.choices[0].message.content
    
    def __repr__(self) -> str:
        return (
            f"Agent("
            f"model={self.model}, "
            f"context={self.context}, "
            f"instructions={self.instructions}"
            f")"
        )

class AgentBuilder:
    def __init__(self, agent_cls: Type[Agent]):
        self.agent_cls = agent_cls
        self.model = None
        self.context = []
        self.instructions = None
        self.params = {}

    def build(self) -> Agent:
        assert self.model is not None, "Model must be specified"
        return self.agent_cls(
            self.model, 
            self.context, 
            self.instructions,
            self.params
        )

    def with_model(self, model: str) -> 'AgentBuilder':
        self.model = model
        return self
    
    def with_context(self, context: list[dict[str, Any]]):
        self.context = context
        return self

    def with_instructions(self, instructions: str):
        self.instructions = instructions
        return self
    
    def with_params(self, params: dict[str, Any]):
        self.params = params
        return self