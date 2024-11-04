from abc import ABC, abstractmethod
from dataclasses import dataclass
from typing import List

from corpora_ai.prompts import SUMMARIZE_SYSTEM_MESSAGE


@dataclass
class ChatCompletionTextMessage:
    """
    Represents a message in a conversation, with a specific role and content.
    """

    role: str  # e.g., "user", "system", "assistant"
    content: str  # The message content


class LLMBaseInterface(ABC):
    """
    Abstract base class for LLM providers, defining methods for text generation and embeddings.
    """

    @abstractmethod
    def get_text_completion(self, messages: List[ChatCompletionTextMessage]) -> str:
        """
        Generates a text completion based on a list of Message objects.

        Args:
            messages (List[Message]): A list of Message objects, each with a role and content.

        Returns:
            str: The generated response text.
        """
        pass

    @abstractmethod
    def get_embedding(self, text: str) -> List[float]:
        """
        Generates an embedding vector for the input text, suitable for a pgvector VectorField.

        Args:
            text (str): The text to embed.

        Returns:
            List[float]: The embedding vector.
        """
        pass

    def get_summary(self, text: str) -> str:
        """
        Generates a summary of the input text.

        Args:
            text (str): The text to summarize.

        Returns:
            str: The generated summary text.
        """
        return self.get_text_completion(
            [
                ChatCompletionTextMessage(
                    role="system",
                    content=SUMMARIZE_SYSTEM_MESSAGE,
                ),
                ChatCompletionTextMessage(
                    role="user",
                    content=f"Summarize the following:\n {text}",
                ),
            ]
        )
