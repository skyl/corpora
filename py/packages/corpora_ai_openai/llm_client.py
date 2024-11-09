import json
from typing import List, Type, TypeVar
from openai import OpenAI, OpenAIError
from pydantic import BaseModel

from corpora_ai.llm_interface import LLMBaseInterface, ChatCompletionTextMessage


T = TypeVar("T", bound=BaseModel)


class OpenAIClient(LLMBaseInterface):
    def __init__(
        self,
        api_key: str,
        completion_model: str = "gpt-4o",
        embedding_model: str = "text-embedding-3-small",
    ):
        self.client = OpenAI(api_key=api_key)
        self.completion_model = completion_model
        self.embedding_model = embedding_model

    def get_text_completion(self, messages: List[ChatCompletionTextMessage]) -> str:
        if not messages:
            raise ValueError("Input messages must not be empty.")
        # Convert Message objects to dictionaries for the OpenAI API
        message_dicts = [{"role": msg.role, "content": msg.content} for msg in messages]
        response = self.client.chat.completions.create(
            model=self.completion_model, messages=message_dicts
        )
        return response.choices[0].message.content

    def get_data_completion(
        self, messages: List[ChatCompletionTextMessage], model: Type[T]
    ) -> T:
        """
        Generates structured data completion using OpenAI's function calling.

        Args:
            messages (List[ChatCompletionTextMessage]): Input messages for the completion.
            model (Type[BaseModel]): A Pydantic model class to validate and structure the output.

        Returns:
            BaseModel: An instance of the provided Pydantic model populated with data.
        """
        if not issubclass(model, BaseModel):
            raise ValueError("Schema must be a subclass of pydantic.BaseModel.")

        if not messages:
            raise ValueError("Input messages must not be empty.")

        # Prepare messages for OpenAI API
        message_dicts = [{"role": msg.role, "content": msg.content} for msg in messages]

        # Generate JSON Schema from the Pydantic model
        json_schema = model.model_json_schema()

        # Define the function for OpenAI's function calling
        function = {
            "name": "generate_data",
            "description": "Generate data based on the provided schema.",
            "parameters": json_schema,
        }

        try:
            # Call OpenAI API with function calling
            response = self.client.chat.completions.create(
                model=self.completion_model,
                messages=message_dicts,
                functions=[function],
                function_call={"name": "generate_data"},
            )

            # Extract and parse function arguments
            function_args = response.choices[0].message.function_call.arguments
            data_dict = json.loads(function_args)
            return model.model_validate(data_dict)
        except OpenAIError as e:
            raise RuntimeError(f"Failed to generate data completion: {e}")
        except json.JSONDecodeError as e:
            raise RuntimeError(f"Failed to parse function arguments: {e}")

    def get_embedding(self, text: str) -> List[float]:
        if not text:
            raise ValueError("Input text must not be empty.")
        response = self.client.embeddings.create(input=text, model=self.embedding_model)
        return response.data[0].embedding
