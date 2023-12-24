from abc import ABC, abstractmethod

from langchain.chains.base import Chain


class BaseUrlslabChainFactory(ABC):

    @abstractmethod
    def create_chain(self) -> Chain:
        """
        Create a chain object. used for completion
        :return: the chain object
        """


