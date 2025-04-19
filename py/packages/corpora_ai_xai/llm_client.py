from typing import List, Type, TypeVar

from corpora_ai.llm_interface import ChatCompletionTextMessage, LLMBaseInterface
from openai import OpenAI, OpenAIError
from pydantic import BaseModel

T = TypeVar("T", bound=BaseModel)


class XAIClient(LLMBaseInterface):
    """
    Grok/XAI client supporting tool-calling (a.k.a. function-calling).
    """

    def __init__(
        self,
        api_key: str,
        completion_model: str = "grok-3-beta",
        embedding_model: str = "text-embedding-3-small",
        base_url: str = "https://api.x.ai/v1",
    ):
        self.client = OpenAI(api_key=api_key, base_url=base_url)
        self.completion_model = completion_model
        self.embedding_model = embedding_model

    def get_text_completion(
        self,
        messages: List[ChatCompletionTextMessage],
    ) -> str:
        if not messages:
            raise ValueError("Input messages must not be empty.")
        payload = [{"role": m.role, "content": m.text} for m in messages]
        resp = self.client.chat.completions.create(
            model=self.completion_model,
            messages=payload,
        )
        return resp.choices[0].message.content

    def get_data_completion(
        self,
        messages: List[ChatCompletionTextMessage],
        model: Type[T],
        tool_name: str,
        tool_description: str,
    ) -> T:
        """
        Uses XAI tool-calling to return a Pydantic-validated model.

        Args:
          messages: chat messages
          model: the Pydantic model class for output
          tool_name: name of the tool/function to invoke
          tool_description: description for the tool

        Returns:
          An instance of `model` populated from the tool_call arguments.
        """
        if not issubclass(model, BaseModel):
            raise ValueError("Schema must subclass pydantic.BaseModel.")
        if not messages:
            raise ValueError("Input messages must not be empty.")

        payload = [{"role": m.role, "content": m.text} for m in messages]
        schema = model.model_json_schema()
        # XAI expects a `tools` list with function definitions:
        tool_def = {
            "type": "function",
            "function": {
                "name": tool_name,
                "description": tool_description,
                "parameters": schema,
            },
        }

        try:
            resp = self.client.chat.completions.create(
                model=self.completion_model,
                messages=payload,
                tools=[tool_def],
                tool_choice={
                    "type": "function",
                    "function": {"name": tool_name},
                },
            )
            msg = resp.choices[0].message
            if not getattr(msg, "tool_calls", None):
                raise RuntimeError("No tool_call in XAI response")
            call = msg.tool_calls[0]
            if call.function.name != tool_name:
                raise RuntimeError(f"Unexpected tool: {call.function.name}")

            # The arguments are a JSON string:
            data = model.model_validate_json(call.function.arguments)
            return data

        except OpenAIError as e:
            raise RuntimeError(f"XAI request failed: {e}")

    def get_embedding(self, text: str) -> List[float]:
        if not text:
            raise ValueError("Input text must not be empty.")
        resp = self.client.embeddings.create(
            input=text,
            model=self.embedding_model,
        )
        return resp.data[0].embedding
