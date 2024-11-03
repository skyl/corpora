from typing import List
from openai import OpenAI

from corpora_ai.llm_interface import LLMBaseInterface, ChatCompletionTextMessage


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

    def generate_embedding(self, text: str) -> List[float]:
        if not text:
            raise ValueError("Input text must not be empty.")
        response = self.client.embeddings.create(input=text, model=self.embedding_model)
        return response.data[0].embedding
