import datetime
from typing import List, Optional
from uuid import UUID


class UrlslabDocument:
    def __init__(self,
                 document_id: str,
                 title: str,
                 content: str,
                 source: str,
                 tenant_id: Optional[str] = None,
                 point_id: Optional[int] = None,
                 chunk_id: Optional[int] = None,
                 **kwargs):
        self.point_id = point_id
        self.document_id = document_id
        self.title = title
        self.content = content
        self.source = source
        self.tenant_id = tenant_id
        self.chunk_id = chunk_id
        self.vector = kwargs.get('vector') or None
        self.score = kwargs.get('score') or None
        self.updated_at = kwargs.get('updated_at') or datetime.datetime.now().strftime("%Y-%m-%d, %H:%M:%S")

    def copy_as_partial_doc(self, partial_content: str, chunk_id: int):
        """
        Copies the document as a partial document
        :param partial_content: The partial content
        :param chunk_id: The chunk id
        :return: UrlslabDocument The partial document
        """
        return UrlslabDocument(
            point_id=None,
            document_id=self.document_id,
            title=self.title,
            content=partial_content,
            source=self.source,
            tenant_id=self.tenant_id,
            chunk_id=chunk_id,
            vector=None,
            score=None,
            updated_at=self.updated_at,
        )

    def to_dict(self):
        return {
            "point_id": self.point_id,
            "document_id": self.document_id,
            "title": self.title,
            "content": self.content,
            "source": self.source,
            "tenant_id": self.tenant_id,
            "chunk_id": self.chunk_id,
            "vector": self.vector,
            "score": self.score,
            "updated_at": self.updated_at,
        }


def join_document_chunks(docs: list[UrlslabDocument]):
    """
    Joins the document chunks into a single document
    :return: UrlslabDocument The document to be returned
    """
    if len(docs) == 0:
        return None

    # throw exception if there are different document ids
    doc_ids = set([doc.document_id for doc in docs])
    if len(doc_ids) > 1:
        raise ValueError("Cannot join documents with different document ids")

    # same for tenant id
    tenant_ids = set([doc.tenant_id for doc in docs])
    if len(tenant_ids) > 1:
        raise ValueError("Cannot join documents with different tenant ids")

    # sort by chunk id
    docs.sort(key=lambda doc: doc.chunk_id)

    # join the documents
    joined_doc = docs[0]
    for doc in docs[1:]:
        joined_doc.content += doc.content

    joined_doc.chunk_id = None
    return joined_doc
