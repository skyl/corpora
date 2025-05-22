# import ast
import json
import re
from typing import List, Type, TypeVar  # , get_origin

from corpora_ai.llm_interface import (
    ChatCompletionTextMessage,
    GeneratedImage,
    LLMBaseInterface,
)
from openai import OpenAI, OpenAIError
from pydantic import BaseModel

T = TypeVar("T", bound=BaseModel)


def extract_last_arguments_json(text: str) -> str:
    # Remove <think>...</think> and <tool_call>...</tool_call>
    text = re.sub(r"<think>.*?</think>", "", text, flags=re.DOTALL)
    text = re.sub(r"<tool_call>.*?</tool_call>", "", text, flags=re.DOTALL)
    text = text.strip()

    decoder = json.JSONDecoder()
    idx = 0
    last_arguments = None

    while idx < len(text):
        # Skip to the next '{' or '['
        match = re.search(r"[\{\[]", text[idx:])
        if not match:
            break
        start = idx + match.start()
        try:
            obj, end = decoder.raw_decode(text[start:])
            if isinstance(obj, dict) and "arguments" in obj:
                last_arguments = obj["arguments"]
            idx = start + end
        except json.JSONDecodeError:
            idx = start + 1  # Move forward and try again

    if last_arguments is None:
        raise ValueError("No valid tool call with 'arguments' found.")

    return json.dumps(last_arguments, ensure_ascii=False)


# Usage example:
def get_tool_args(msg):
    # Try tool_calls first (if API ever returns it)
    tool_calls = getattr(msg, "tool_calls", None)
    if tool_calls:
        # your normal tool call logic here
        return tool_calls[0].function.arguments
    # Fallback: generic JSON extraction from message content
    return extract_last_arguments_json(msg.content)


class LocalClient(LLMBaseInterface):
    """
    Client for local OpenAI-compatible LLMs (e.g. LM Studio) running on the host machine.
    """

    def __init__(
        self,
        api_key: str = "foobar",  # LM Studio ignores the API key
        completion_model: str = "deepseek-r1-distill-qwen-7b",
        # embedding_model: str = "text-embedding-3-small",  # Optional / placeholder
        # image_model: str = "local-image-model",  # Optional / placeholder
        base_url: str = "http://host.docker.internal:1234/v1",
    ):
        self.client = OpenAI(api_key=api_key, base_url=base_url)
        self.completion_model = completion_model
        # self.embedding_model = embedding_model
        # self.image_model = image_model

    def get_text_completion(
        self,
        messages: List[ChatCompletionTextMessage],
    ) -> str:
        if not messages:
            raise ValueError("Input messages must not be empty.")

        message_dicts = [
            {"role": msg.role, "content": msg.text} for msg in messages
        ]

        response = self.client.chat.completions.create(
            model=self.completion_model,
            messages=message_dicts,
        )
        return response.choices[0].message.content

    def get_data_completion(
        self,
        messages: List[ChatCompletionTextMessage],
        model: Type[T],
        retries: int = 3,
    ) -> T:
        """
        Uses tool-calling to return a Pydantic-validated model.

        Args:
            messages: chat messages
            model: the Pydantic model class for output
            retries: how many times to retry if the tool call fails

        Returns:
            An instance of the model populated from the tool_call arguments.
        """
        if not issubclass(model, BaseModel):
            raise ValueError("Schema must be a subclass of pydantic.BaseModel.")
        if not messages:
            raise ValueError("Input messages must not be empty.")

        tool_name = model.__name__
        tool_description = f"Generate data based on the {tool_name} schema."

        payload = [{"role": msg.role, "content": msg.text} for msg in messages]
        schema = model.model_json_schema()

        tool_def = {
            "type": "function",
            "function": {
                "name": tool_name,
                "description": tool_description,
                "parameters": schema,
            },
        }

        # tool_choice = {
        #     "type": "function",
        #     "function": {
        #         "name": tool_name,
        #     },
        # }

        for attempt in range(retries):
            try:
                response = self.client.chat.completions.create(
                    model=self.completion_model,
                    messages=payload,
                    tools=[tool_def],
                    # TODO: for some reason, LM Studio doesn't like
                    # maybe later version will work.
                    # tool_choice=tool_choice,
                    # tool_choice="required",
                    tool_choice="auto",
                )

                msg = response.choices[0].message

                try:
                    arguments = get_tool_args(msg)
                    return model.model_validate_json(arguments)
                except Exception as e:  # noqa
                    print(f"Failed to validate tool_call arguments: {e}")
                    # print(tool.function.arguments)
                    if attempt == retries - 1:
                        raise RuntimeError(
                            f"Failed to validate tool_call arguments: {e}",
                        )
                    continue

            except OpenAIError as e:
                print(f"Request failed: {e}")
                if attempt == retries - 1:
                    raise RuntimeError(f"Request failed: {e}")
                continue
            except json.JSONDecodeError as e:
                print(f"Failed to parse tool_call arguments: {e}")
                if attempt == retries - 1:
                    raise RuntimeError(
                        f"Failed to parse tool_call arguments: {e}",
                    )
                continue

    def get_image(
        self,
        prompt: str,
        **kwargs,
    ) -> List[GeneratedImage]:
        raise NotImplementedError(
            "Image generation is not supported by this local client.",
        )

    def get_embedding(self, text: str) -> List[float]:
        raise NotImplementedError(
            "Embeddings are not supported by this local client.",
        )
