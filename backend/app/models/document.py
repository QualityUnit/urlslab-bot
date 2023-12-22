from uuid import UUID


class UrlslabDocument:
    def __init__(self,
                 document_id: UUID,
                 title: str,
                 content: str,
                 source: str,
                 tenant_id: int,
                 **kwargs):
        self.document_id = document_id
        self.title = title
        self.content = content
        self.source = source
        self.tenant_id = tenant_id
        self.vector = kwargs.get('vector')
