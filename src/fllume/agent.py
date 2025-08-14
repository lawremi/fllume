import any_llm
import json

import logging
from typing import Any, Callable, Generator, Iterator, Optional, Type, Union
from pydantic import BaseModel
from any_llm.types.completion import (
    ChatCompletionMessage,
    ChatCompletionMessageFunctionToolCall,
    Function
)

logger = logging.getLogger(__name__)

class Agent:
    """An LLM-powered agent that can complete prompts, use tools, and more.

    The Agent class is the main entry point for interacting with large language
    models. It can be configured with specific instructions, tools, response
    formats, and other parameters to tailor its behavior for specific tasks.

    It is recommended to create Agent instances using the fluent `AgentBuilder`
    by calling `Agent.builder()`.
    """
    def __init__(
        self, 
        model: str, 
        instructions: Optional[str] = None, 
        tools: Optional[list[Callable[..., Any]]] = None,
        response_format: Optional[Union[dict[str, Any], type[BaseModel]]] = None,
        prompt_template: Optional[str] = None,
        params: Optional[dict[str, Any]] = None,
    ):
        """Initializes the Agent.

        Args:
            model: The identifier of the language model to use (e.g.,
                'ollama/llama3'). See the `any-llm documentation
                <https://mozilla-ai.github.io/any-llm/providers/>`_ for a
                full list of providers, depending on how any-llm was installed.
            instructions: The system-level instructions for the agent.
            tools: A list of Python functions to be used as tools.
                Annotating each function with a docstring and type hints will
                help the model make effective use of them.
            response_format: The desired format for the response, e.g., a
                Pydantic model or a JSON schema.
            prompt_template: A template for formatting dictionary-based
                prompts, as a format string.
            params: Additional parameters to pass to the LLM API.
        """
        self.model = model
        self.tools = tools if tools is not None else []
        self.response_format = response_format
        self.prompt_template = prompt_template
        self.params = params if params is not None else {}
        self.instructions = self._build_instructions(instructions)
        
    @classmethod
    def builder(cls) -> 'AgentBuilder':
        """Creates a new AgentBuilder instance for fluently 
        constructing an Agent.

        Returns:
            An instance of AgentBuilder.
        """
        return AgentBuilder(cls)

    def _build_instructions(self, instructions: Optional[str]) -> str:
        """
        Extends the user-provided instructions to enable tool usage 
        and response formatting.
        """
        base = (
            instructions
            if instructions is not None
            else "You are a helpful and concise assistant."
        )
        parts = [base]
        if self.tools:
            parts.append("Use tools when relevant or requested.")
        if self.response_format:
            if self.tools:
                parts.append(
                    "When you are finished with tool calls, your final "
                    "response must be in a JSON format."
                )
            else:
                parts.append(
                    "You must output your response in a JSON format."
                )
        return " ".join(parts)

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

    def _build_user_message(
        self, prompt: Union[str, dict[str, Any], None]
    ) -> list[dict[str, Any]]:
        """Builds the user message list from a string or dictionary prompt."""
        prompt_str: Optional[str]
        if isinstance(prompt, dict):
            if not self.prompt_template:
                raise ValueError(
                    "A dict prompt was provided, but the agent has no "
                    "prompt_template."
                )
            prompt_str = self.prompt_template.format(**prompt)
        else:
            prompt_str = prompt  # It's a string or None

        return [{"role": "user", "content": prompt_str}] if prompt_str else []

    def complete_with_context(
        self, 
        context: Optional[list[dict[str, Any]]] = None,
        prompt: Union[str, dict[str, Any], None] = None,
        stream: bool = False
    ) -> Union[list[dict[str, Any]], Generator[dict[str, Any], None, None]]:
        """Executes a completion within a given conversational context.

        This method is used for multi-turn interactions. The `context` returned
        from one call should be passed as the `context` argument in the next
        call to maintain the conversational history.

        Args:
            context: The list of messages representing the conversation
                history.
            prompt: The new user prompt to add to the conversation.
            stream: If True, the response will be returned as a generator of
                message objects. Defaults to False.

        Returns:
            If streaming, a generator that yields message objects. If not
            streaming, the updated context list including the new user prompt
            and the assistant's response.
        """
        if context is None:
            context = [{"role": "system", "content": self.instructions}]

        # Convert any ChatCompletionMessages in the message history to dicts
        # before sending them to the any-llm API, which expects dicts.
        context_as_dicts = [
            (
                msg.model_dump(exclude_none=True) 
                if isinstance(msg, BaseModel) else msg
            )
            for msg in context
        ]
        
        user_message = self._build_user_message(prompt)
        completion = any_llm.completion(
            self.model,
            messages=context_as_dicts + user_message,
            stream=stream,
            tools = self.tools,
            response_format=self.response_format,
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
    ) -> str:
        """Executes a tool function, catching any exceptions and returning 
        any error messages to the LLM."""
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
        return str(content)

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
    
    def _get_final_response(
        self, completion_context: list[Any]
    ) -> Union[str, BaseModel, dict[str, Any]]:
        last_message = completion_context[-1]
        if not self.response_format:
            return last_message.content

        parsed_data = last_message.parsed
        if (
            isinstance(self.response_format, type)
            and issubclass(self.response_format, BaseModel)
        ):
            return self.response_format(**parsed_data)
        return parsed_data

    def complete(
        self, prompt: Union[str, dict[str, Any]], stream: bool = False
    ) -> Union[str, Generator[str, None, None], BaseModel, dict[str, Any]]:
        """Executes a prompt and returns the agent's response.

        This is the primary method for interacting with the agent. It takes a
        prompt, sends it to the LLM (along with any configured context, tools,
        etc.), and returns the final response.

        Args:
            prompt: The user prompt. Can be a string or a dictionary if the
                agent was configured with a `prompt_template`.
            stream: If True, the response will be returned as a generator of
                string chunks. Defaults to False.

        Returns:
            The agent's response, which can be a string, a Pydantic model, a
            dictionary, or a generator of strings if streaming.
        """
        completion = self.complete_with_context(prompt=prompt, stream=stream)
        if stream:
            return self._stream_content(completion)
        else:
            return self._get_final_response(completion)

    def __repr__(self) -> str:
        tool_names = [tool.__name__ for tool in self.tools]
        response_format_repr = (
            self.response_format.__name__
            if isinstance(self.response_format, type)
            else repr(self.response_format)
        )
        return (
            f"Agent("
            f"model='{self.model}', "
            f"instructions='{self.instructions}', "
            f"tools={tool_names}, "
            f"response_format={response_format_repr}, "
            f"prompt_template='{self.prompt_template}', "
            f"params={self.params}"
            f")"
        )

class AgentBuilder:
    """A fluent builder for creating and configuring Agent instances."""
    def __init__(self, agent_cls: Type[Agent]):
        """Initializes the AgentBuilder.

        Args:
            agent_cls: The Agent class to be instantiated by the builder.
        """
        self.agent_cls = agent_cls
        self.model = None
        self.instructions = None
        self.response_format = None
        self.prompt_template = None
        self.params = {}
        self.tools = []
        
    def build(self) -> Agent:
        """Builds and returns a configured Agent instance.

        Returns:
            A new Agent instance with the specified configuration.
        """
        assert self.model is not None, "Model must be specified"
        return self.agent_cls(
            self.model, 
            self.instructions,
            self.tools,
            self.response_format,
            self.prompt_template,
            self.params
        )

    def with_model(self, model: str) -> 'AgentBuilder':
        """Sets the language model for the agent.

        Args:
            model: The identifier of the language model to use (e.g.,
                "ollama/llama3").  See the `any-llm documentation
                <https://mozilla-ai.github.io/any-llm/providers/>`_ for a
                full list of providers, depending on how any-llm was installed.

        Returns:
            The AgentBuilder instance for chaining.
        """
        self.model = model
        return self

    def with_instructions(self, instructions: str) -> "AgentBuilder":
        """Sets the system-level instructions for the agent.

        Args:
            instructions: A string containing the instructions that guide the
                agent's behavior.

        Returns:
            The AgentBuilder instance for chaining.
        """
        self.instructions = instructions
        return self
    
    def with_tools(self, tools: list[Callable[..., Any]]) -> "AgentBuilder":
        """Provides a list of Python functions to be used as tools by the agent.

        Args:
            tools: A list of callable Python functions.

        Returns:
            The AgentBuilder instance for chaining.
        """
        self.tools = tools
        return self

    def with_response_format(
        self, response_format: Union[dict[str, Any], type[BaseModel]]
    ) -> "AgentBuilder":
        """Specifies the desired format for the agent's response.

        Args:
            response_format: A Pydantic model or a JSON schema dictionary that
                defines the structure of the output.

        Returns:
            The AgentBuilder instance for chaining.
        """
        self.response_format = response_format
        return self

    def with_prompt_template(self, template: str) -> "AgentBuilder":
        """Sets a prompt template for formatting dictionary-based prompts.

        Args:
            template: A format string (e.g., "Summarize: {text}").

        Returns:
            The AgentBuilder instance for chaining.
        """
        self.prompt_template = template
        return self

    def with_params(self, params: dict[str, Any]) -> "AgentBuilder":
        """Sets additional parameters to be passed to the LLM API.

        Args:
            params: A dictionary of parameters (e.g., {"temperature": 0.7}).

        Returns:
            The AgentBuilder instance for chaining.
        """
        self.params = params
        return self