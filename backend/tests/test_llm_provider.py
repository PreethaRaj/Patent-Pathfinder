from backend.llm.provider import build_llm_provider

class Settings:
    llm_provider = "vllm"
    vllm_base_url = "http://localhost:8001"
    ollama_base_url = "http://localhost:11434"
    chat_model = "llama3.1"
    ollama_chat_model = "mistral-nemo"
    embedding_model = "bge-large-en-v1.5"

def test_build_vllm_provider():
    provider = build_llm_provider(Settings())
    assert provider.__class__.__name__ == "VLLMClient"

def test_build_ollama_provider():
    s = Settings()
    s.llm_provider = "ollama"
    provider = build_llm_provider(s)
    assert provider.__class__.__name__ == "OllamaClient"
