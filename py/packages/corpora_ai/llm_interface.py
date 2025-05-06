from abc import ABC, abstractmethod
from dataclasses import dataclass
from typing import List, Optional, Type, TypeVar

from pydantic import BaseModel

from corpora_ai.prompts import (
    SUMMARIZE_SYSTEM_MESSAGE,
    SYNTHETIC_EMBEDDING_SYSTEM_MESSAGE,
)

T = TypeVar("T", bound=BaseModel)


@dataclass
class ChatCompletionTextMessage:
    """Represents a message in a conversation, with a specific role and text."""

    role: str  # e.g., "user", "system", "assistant"
    text: str


@dataclass
class GeneratedImage:
    """Holds one generated image's raw bytes plus an optional format hint."""

    data: bytes
    format: Optional[str] = "png"


class LLMBaseInterface(ABC):
    """Abstract base class for LLM providers, defining methods for text generation and embeddings."""

    @abstractmethod
    def get_text_completion(
        self,
        messages: List[ChatCompletionTextMessage],
    ) -> str:
        """Generates a text completion based on a list of Message objects.

        Args:
            messages (List[Message]): A list of Message objects, each with a role and content.

        Returns:
            str: The generated response text.

        """

    @abstractmethod
    def get_data_completion(
        self,
        messages: List[ChatCompletionTextMessage],
        model: Type[T],
    ) -> T:
        """Generates an instance of the provided schema based on a list of Message objects.

        Args:
            messages (List[Message]): A list of Message objects, each with a role and content.
            schema (Type[T]): The type to populate with the generated data.

        Returns:
            T: The generated instance of the schema type.

        """

    @abstractmethod
    def get_image(
        self,
        prompt: str,
        **kwargs,
    ) -> List[GeneratedImage]:
        """Generate `n` images of size 1024x768 px from the given text prompt.

        Args:
            prompt: Natural-language description of the desired image.
            kwargs: arguments to pass to the image generation API.

        Returns:
            A list of GeneratedImage with raw bytes and the appropriate format.
        """

    @abstractmethod
    def get_embedding(self, text: str) -> List[float]:
        """Generates an embedding vector for the input text, suitable for a pgvector VectorField.

        Args:
            text (str): The text to embed.

        Returns:
            List[float]: The embedding vector.

        """

    def get_summary(self, text: str) -> str:
        """Generates a summary of the input text.

        Args:
            text (str): The text to summarize.

        Returns:
            str: The generated summary text.

        """
        return self.get_text_completion(
            [
                ChatCompletionTextMessage(
                    role="system",
                    text=SUMMARIZE_SYSTEM_MESSAGE,
                ),
                ChatCompletionTextMessage(
                    role="user",
                    text=f"Summarize the following:\n {text}",
                ),
            ],
        )

    def get_synthetic_embedding_text(self, text: str) -> str:
        """Given a short prompt, generate a synthetic embedding text
        that is more like to match splits in the corpus.
        """
        return self.get_text_completion(
            [
                ChatCompletionTextMessage(
                    role="system",
                    text=SYNTHETIC_EMBEDDING_SYSTEM_MESSAGE,
                ),
                ChatCompletionTextMessage(
                    role="user",
                    text=text,
                ),
            ],
        )
