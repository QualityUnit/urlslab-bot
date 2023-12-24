from abc import ABC, abstractmethod


class BinaryContentReader(ABC):
    """Abstract base class to define the interface for content readers."""

    def __init__(self, binary_content: bytes):
        self.binary_content = binary_content

    @abstractmethod
    def read(self) -> str:
        """Read the binary content and return the parsed data."""
        pass
