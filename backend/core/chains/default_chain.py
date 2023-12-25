from operator import itemgetter

from langchain.chains.base import Chain
from langchain_core.output_parsers import StrOutputParser
from langchain_core.prompts import ChatPromptTemplate, PromptTemplate
from langchain_core.runnables import RunnablePassthrough, RunnableLambda

from backend.app.models import ChatSession
from backend.app.repositories.document import DocumentRepository
from backend.core.chains.base import BaseUrlslabChainFactory
from backend.core.chains.templates import RAG_CHAT_TEMPLATE


class DefaultChainFactory(BaseUrlslabChainFactory):

    def __init__(self,
                 document_repository: DocumentRepository,
                 session: ChatSession,
                 user_id: int):
        self.document_repository = document_repository
        self.session = session
        self.user_id = user_id
        self.sources = []

    def create_chain(self) -> Chain:
        model = self.session.ai_model_settings.chat_model.langchain_model
        prompt = PromptTemplate.from_template(
            RAG_CHAT_TEMPLATE,
        )

        history_prompt = ChatPromptTemplate.from_messages(
            self.session.message_history,
        )

        # all needed components are created - creating chain
        return (
            {
                "context": itemgetter("human_input") | RunnableLambda(self._retrieve_documents),
                "human_input": RunnablePassthrough(),
                "history": history_prompt,
            }
            | prompt
            | model
            | StrOutputParser()
        )

    async def _retrieve_documents(self, query: str):
        query_vector = await self.session.ai_model_settings.embedding_model.aembed_query(query)
        documents = await self.document_repository.search_by_tenant_id(self.user_id,
                                                                       self.session.tenant_id,
                                                                       query_vector,
                                                                       score_threshold=0.8)

        context = ""
        for doc in documents:
            context += doc.content + " "

        # save the sources
        self.sources = [doc.document_id for doc in documents]

        return context
