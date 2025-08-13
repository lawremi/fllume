import any_llm
import json
import logging
from typing import Any, Callable, Generator, Iterator, Optional, Type, Union
from any_llm.types.completion import (
    ChatCompletionMessage,
    ChatCompletionMessageFunctionToolCall,
    Function
)

logger = logging.getLogger(__name__)

class Agent:
    def __init__(
        self, 
        model: str, 
        instructions: Optional[str] = None, 
        tools: Optional[list[Callable[..., Any]]] = None,
        params: Optional[dict[str, Any]] = None,
    ):
        self.model = model
        self.instructions = (
            instructions
            if instructions is not None
            else "You are a helpful and concise assistant."
        )
        self.tools = tools if tools is not None else []
        if self.tools:
            self.instructions += " Use tools when relevant or requested."
        self.params = params if params is not None else {}
        
    @classmethod
    def builder(cls) -> 'AgentBuilder':
        return AgentBuilder(cls)

    def _stream_messages(
        self, completions: Iterator[Any],
        context: list[dict[str, Any]]
    ) -> Generator[dict[str, Any], None, None]:
        """
        Helper generator method to extract messages from
        any_llm.completion().
        """
        tool_calls = []
        
        for chunk in completions:
            delta = chunk.choices[0].delta
            assert not (delta.content and tool_calls), (
                "Received a content chunk after a tool call was "
                "already initiated in the stream."
            )
            
            if delta.tool_calls:
                for tool_call_delta in delta.tool_calls:
                    index = tool_call_delta.index
                    if index == len(tool_calls):
                        # New tool call - append the delta
                        tool_calls.append(tool_call_delta)
                    else:
                        # Continuation - merge arguments
                        tool_calls[index].function.arguments += (
                            tool_call_delta.function.arguments
                        )
            else:
                yield delta
        
        if tool_calls:
            completed_tool_calls = [
                ChatCompletionMessageFunctionToolCall(
                    id = tc.id,
                    function = Function(
                        name = tc.function.name,
                        arguments = tc.function.arguments
                    ),
                    type = 'function'
                )
                for tc in tool_calls
            ]
            message = ChatCompletionMessage(
                role = 'assistant',
                content = None,
                tool_calls = completed_tool_calls
            )
            yield from self._handle_tool_calls(message, context, stream=True)

    def _stream_content(
        self, completions: Generator[dict[str, Any], None, None]
    ) -> Generator[str, None, None]:
        """
        Helper generator method to extract content from 
        _stream_messages().
        """
        for chunk in completions:
            if chunk.content is not None:
                yield chunk.content
        
    def complete_with_context(
        self, 
        context: Optional[list[dict[str, Any]]] = None,
        prompt: Optional[str] = None,
        stream: bool = False
    ) -> Union[list[dict[str, Any]], Generator[dict[str, Any], None, None]]:
        context = context if context is not None else []
        user_message = [{"role": "user", "content": prompt}] if prompt else []
        completion = any_llm.completion(
            self.model,
            messages = context + user_message,
            stream = stream,
            tools = self.tools,
            **self.params
        )
        if stream:
            return self._stream_messages(completion, context)
        else:
            message = completion.choices[0].message
            return self._handle_tool_calls(message, context)

    def _handle_tool_calls(
        self, message: Any, context: list[dict[str, Any]],
        stream: bool = False
    ) -> Union[list[dict[str, Any]], Generator[dict[str, Any], None, None]]:
        """
        Recursively handles tool calls until a final response is generated.
        """
        context = context + [message]
        if message.tool_calls:
            tool_messages = self._call_tools(message.tool_calls)
            context = self.complete_with_context(
                context + tool_messages,
                stream=stream
            )
        return context

    def _execute_tool_call(
        self, 
        tool_function: Callable[..., Any], 
        arguments: dict[str, Any]
    ) -> Any:
        try:
            content = tool_function(**arguments)
        except Exception as e:
            logger.debug(
                "Error executing tool %s with arguments %s.",
                tool_function.__name__,
                arguments,
                exc_info=True
            )
            content = f"Error executing tool: {e}" # Return error msg to LLM
        return content

    def _call_tools(self, tool_calls: list[Any]) -> list[dict[str, Any]]:
        tool_dict = {tool.__name__: tool for tool in self.tools}
        tool_messages = [
            {
                "role": "tool",
                "tool_call_id": tool_call.id,
                "content": self._execute_tool_call(
                    tool_dict[tool_call.function.name],
                    json.loads(tool_call.function.arguments)
                ),
            }
            for tool_call in tool_calls
        ]
        return tool_messages
    
    def complete(
        self, prompt: str, stream: bool = False
    ) -> Union[str, Generator[str, None, None]]:
        context = [{"role": "system", "content": self.instructions}]
        completion = self.complete_with_context(context, prompt, stream)
        if stream:
            return self._stream_content(completion)
        else:
            return completion[-1].content
            
    def __repr__(self) -> str:
        tool_names = [tool.__name__ for tool in self.tools]
        return (
            f"Agent("
            f"model='{self.model}', "
            f"instructions='{self.instructions}', "
            f"tools={tool_names}, "
            f"params={self.params}"
            f")"
        )

class AgentBuilder:
    def __init__(self, agent_cls: Type[Agent]):
        self.agent_cls = agent_cls
        self.model = None
        self.instructions = None
        self.params = {}
        self.tools = []
        
    def build(self) -> Agent:
        assert self.model is not None, "Model must be specified"
        return self.agent_cls(
            self.model, 
            self.instructions,
            self.tools,
            self.params
        )

    def with_model(self, model: str) -> 'AgentBuilder':
        self.model = model
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