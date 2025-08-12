import any_llm
from typing import Type, Iterator, Union, Generator, Any, Callable

class Agent:
    def __init__(
        self, 
        model: str, 
        context: list[dict[str, Any]], 
        instructions: str, 
        tools: list[Callable[..., Any]],
        params: dict[str, Any]
    ):
        self.model = model
        self.context = context
        self.instructions = instructions
        self.tools = tools
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

    def complete_with_context(
        self, 
        context: list[dict[str, Any]] = [],
        stream: bool = False
    ):
        completion = any_llm.completion(
            self.model, 
            messages = context,
            stream = stream,
            tools = self.tools
            **self.params
        )
        if stream:
            return self._stream_completion(completion)
        else:
            return context + completion.choices[0].message

    def _call_tools(self, tool_calls: dict[str, Any]):
        tool_dict = {tool.__name__: tool for tool in self.tools}
        tool_messages = [
            {
                "role": "tool",
                "tool_call_id": tool_call.id,
                "content": tool_dict[tool_call.function.name](
                    **tool_call.function.arguments
                )
            }
            for tool_call in tool_calls
        ]
        return tool_messages
    
    def complete(
        self, prompt: str, stream: bool = False
    ) -> Union[str, Generator[str, None, None]]:
        context = (
            self.context
            + (
                [{"role": "system", "content": self.instructions}] 
                if self.instructions else []
            )
            + [{"role": "user", "content": prompt}]
        )
        completion = self.complete_with_context(context, stream)
        if stream:
            return completion
        else:
            while len(completion[-1].tool_calls) > 0:
                tool_messages = self._call_tools(completion[-1].tool_calls)
                completion = self.complete_with_context(completion + tool_messages)
            return completion[-1].content
            
    def __repr__(self) -> str:
        return (
            f"Agent("
            f"model={self.model}, "
            f"context={self.context}, "
            f"instructions={self.instructions}, "
            f"tools={self.tools}, "
            f"params={self.params}"
            f")"
        )

class AgentBuilder:
    def __init__(self, agent_cls: Type[Agent]):
        self.agent_cls = agent_cls
        self.model = None
        self.context = []
        self.instructions = None
        self.params = {}
        self.tools = []
        
    def build(self) -> Agent:
        assert self.model is not None, "Model must be specified"
        return self.agent_cls(
            self.model, 
            self.context, 
            self.instructions,
            self.tools,
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
    
    def with_tools(self, tools: list[Callable[..., Any]]):
        self.tools = tools
        return self

    def with_params(self, params: dict[str, Any]):
        self.params = params
        return self