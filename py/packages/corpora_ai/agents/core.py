from typing import Generic, Optional, TypeVar

from pydantic import BaseModel

InputType = TypeVar("InputType", bound=BaseModel)
OutputType = TypeVar("OutputType", bound=BaseModel)
ContextType = TypeVar("ContextType", bound=BaseModel)


class Agent(Generic[InputType, OutputType, ContextType]):
    """
    A core AI Agent.
    Given an InputType, produces an OutputType,
    optionally using an injected typed context.
    """

    name: str

    def run(
        self,
        input: InputType,
        context: Optional[ContextType] = None,
    ) -> OutputType: ...
