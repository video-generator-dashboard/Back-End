from abc import ABC, abstractmethod
from typing import Any, Dict, List, Optional


class BaseProvider(ABC):
    @abstractmethod
    async def __call__(self, prompt: str, **generation_args: Any) -> str:
        """
        Generate a response based on the provided prompt and generation arguments.
        """
        pass