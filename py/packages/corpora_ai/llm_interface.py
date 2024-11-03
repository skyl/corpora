from abc import ABC, abstractmethod
from dataclasses import dataclass
from typing import List


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
    def generate_embedding(self, text: str) -> List[float]:
        """
        Generates an embedding vector for the input text, suitable for a pgvector VectorField.

        Args:
            text (str): The text to embed.

        Returns:
            List[float]: The embedding vector.
        """
        pass
