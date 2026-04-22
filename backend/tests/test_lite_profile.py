from backend.core.config import Settings


def test_lite_settings_flags():
    settings = Settings(APP_EDITION="lite", ENVIRONMENT="production", LLM_PROVIDER="ollama")
    assert settings.is_lite is True
    assert settings.environment == "production"
    assert settings.llm_provider == "ollama"
