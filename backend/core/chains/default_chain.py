from langchain.chains.base import Chain

from backend.app.models import ChatSession
from backend.core.chains.base import BaseUrlslabChainFactory


class DefaultChainFactory(BaseUrlslabChainFactory):

    def __init__(self, session: ChatSession):
        self.session = session

    def create_chain(self) -> Chain:
        pass
