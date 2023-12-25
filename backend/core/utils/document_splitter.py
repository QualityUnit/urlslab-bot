import tiktoken
from langchain.text_splitter import TokenTextSplitter

from backend.app.models.aimodel import UrlslabEmbeddingModel
from backend.app.models.document import UrlslabDocument


class UrlslabDocumentSplitter:
    def __init__(self, documents: list[UrlslabDocument]):
        self.documents = documents

    def split(self, chunk_size: int = 2000, chunk_overlap: int = 200):
        returning_docs = []
        for document in self.documents:
            texts = self._split_text(chunk_size, chunk_overlap, document.content)
            for chunk_id, doc_part in enumerate(texts, start=1):
                returning_docs.append(document.copy_as_partial_doc(doc_part, chunk_id))
        return returning_docs

    def token_count(self):
        """
        Returns the token count of the documents all together
        :return:  The token count of the documents
        """
        count = 0
        encoder = tiktoken.get_encoding('gpt2')
        for document in self.documents:
            count += len(encoder.encode(document.content))
        return count

    @staticmethod
    def _split_text(chunk_size: int,
                    chunk_overlap: int,
                    document: str) -> list[str]:
        text_chunks = TokenTextSplitter.from_tiktoken_encoder(chunk_size=chunk_size,
                                                              chunk_overlap=chunk_overlap).split_text(document)
        return text_chunks

    @staticmethod
    async def vectorize_text(text: str, embedding_model: UrlslabEmbeddingModel):
        chunk_size = embedding_model.embedding_dimensions()
        chunk_overlap = 0
        text_chunks = TokenTextSplitter.from_tiktoken_encoder(chunk_size=chunk_size,
                                                              chunk_overlap=chunk_overlap).split_text(text)
        return await embedding_model.aembed_query(text_chunks[0])

