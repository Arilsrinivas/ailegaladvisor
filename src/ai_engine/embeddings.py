from langchain_huggingface import HuggingFaceEmbeddings
from src.core.config import settings

_embeddings_instance = None

def get_embeddings_model() -> HuggingFaceEmbeddings:
    global _embeddings_instance
    if _embeddings_instance is None:
        _embeddings_instance = HuggingFaceEmbeddings(
            model_name=settings.EMBEDDING_MODEL,
            cache_folder=settings.EMBEDDING_CACHE_DIR
        )
    return _embeddings_instance
