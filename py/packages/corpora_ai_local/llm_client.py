import json
from typing import List, Type, TypeVar

from corpora_ai.llm_interface import (
    ChatCompletionTextMessage,
    GeneratedImage,
    LLMBaseInterface,
)
from openai import OpenAI, OpenAIError
from pydantic import BaseModel

T = TypeVar("T", bound=BaseModel)


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
                    tool_choice="auto",
                )

                msg = response.choices[0].message
                tool_calls = getattr(msg, "tool_calls", None)
                if not tool_calls:
                    print("No tool_call in response.")
                    if attempt == retries - 1:
                        raise RuntimeError("No tool_call in response.")
                    continue

                tool = tool_calls[0]
                # if tool.function.name != tool_name:
                #     print(
                #         f"Unexpected tool name: {tool.function.name} "
                #         f"(expected: {tool_name})",
                #     )
                #     if attempt == retries - 1:
                #         raise RuntimeError(
                #             f"Unexpected tool name: {tool.function.name}",
                #         )
                #     continue

                return model.model_validate_json(tool.function.arguments)

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
