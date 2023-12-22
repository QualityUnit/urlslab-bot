class AIModel:
    def __init__(self,
                 embedding_model_class: str,
                 embedding_model_name: str,
                 llm_model_class: str,
                 llm_model_name: str):
        self.embedding_model_class = embedding_model_class
        self.embedding_model_name = embedding_model_name
        self.llm_model_class = llm_model_class
        self.llm_model_name = llm_model_name
