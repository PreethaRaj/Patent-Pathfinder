from backend.llm.base import LLMProvider
from backend.llm.ollama_client import OllamaClient
from backend.llm.vllm_client import VLLMClient

def build_llm_provider(settings) -> LLMProvider:
    provider = settings.llm_provider.lower()
    if provider in {"vllm", "llama"}:
        return VLLMClient(
            base_url=settings.vllm_base_url,
            chat_model=settings.chat_model,
            embedding_model=settings.embedding_model,
        )
    if provider in {"ollama", "mistral"}:
        return OllamaClient(
            base_url=settings.ollama_base_url,
            chat_model=settings.ollama_chat_model,
            embedding_model="nomic-embed-text",
        )
    raise ValueError(f"Unsupported LLM_PROVIDER: {settings.llm_provider}")
