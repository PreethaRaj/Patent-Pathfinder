from functools import lru_cache

from pydantic import Field
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file='.env', env_file_encoding='utf-8', extra='ignore')

    app_name: str = 'Intelligent Innovation Copilot'
    app_edition: str = Field(default='full', alias='APP_EDITION')
    environment: str = Field(default='development', alias='ENVIRONMENT')

    llm_provider: str = Field(default='vllm', alias='LLM_PROVIDER')
    vllm_base_url: str = Field(default='http://vllm:8000', alias='VLLM_BASE_URL')
    ollama_base_url: str = Field(default='http://ollama:11434', alias='OLLAMA_BASE_URL')
    embedding_model: str = Field(default='bge-large-en-v1.5', alias='EMBEDDING_MODEL')
    chat_model: str = Field(default='meta-llama/Llama-3.1-70B-Instruct', alias='CHAT_MODEL')
    ollama_chat_model: str = Field(default='mistral-nemo', alias='OLLAMA_CHAT_MODEL')

    database_url: str = Field(default='postgresql+psycopg://innovation:innovation@postgres:5432/innovation', alias='DATABASE_URL')
    opensearch_url: str = Field(default='http://opensearch:9200', alias='OPENSEARCH_URL')
    opensearch_index: str = Field(default='innovation-documents', alias='OPENSEARCH_INDEX')
    neo4j_url: str = Field(default='bolt://neo4j:7687', alias='NEO4J_URL')
    neo4j_username: str = Field(default='neo4j', alias='NEO4J_USERNAME')
    neo4j_password: str = Field(default='neo4jpassword', alias='NEO4J_PASSWORD')
    redis_url: str = Field(default='redis://redis:6379/0', alias='REDIS_URL')

    jwt_secret: str = Field(default='change-me', alias='JWT_SECRET')
    jwt_algorithm: str = Field(default='HS256', alias='JWT_ALGORITHM')
    jwt_audience: str = Field(default='intelligent-innovation-copilot', alias='JWT_AUDIENCE')
    jwt_issuer: str = Field(default='http://localhost', alias='JWT_ISSUER')

    mcp_retrieval_url: str = Field(default='http://mcp_retrieval:8101', alias='MCP_RETRIEVAL_URL')
    mcp_ingestion_url: str = Field(default='http://mcp_ingestion:8102', alias='MCP_INGESTION_URL')
    mcp_evidence_url: str = Field(default='http://mcp_evidence:8103', alias='MCP_EVIDENCE_URL')
    mcp_novelty_url: str = Field(default='http://mcp_novelty:8104', alias='MCP_NOVELTY_URL')
    mcp_monitoring_url: str = Field(default='http://mcp_monitoring:8105', alias='MCP_MONITORING_URL')
    mcp_report_url: str = Field(default='http://mcp_report:8106', alias='MCP_REPORT_URL')

    otel_exporter_otlp_endpoint: str | None = Field(default=None, alias='OTEL_EXPORTER_OTLP_ENDPOINT')
    prometheus_multiproc_dir: str | None = Field(default=None, alias='PROMETHEUS_MULTIPROC_DIR')
    celery_broker_url: str = Field(default='redis://redis:6379/1', alias='CELERY_BROKER_URL')
    cors_origins: list[str] = [
    "http://localhost:3000",
    "http://127.0.0.1:3000",
    "http://localhost:3186",
    "http://127.0.0.1:3186",
    "http://localhost:5005",
    "http://127.0.0.1:5005",
    "http://localhost:5006",
    "http://127.0.0.1:5006",
    ]

    patent_source: str = Field(default='lens', alias='PATENT_SOURCE')
    patent_source_fallback: str = Field(default='none', alias='PATENT_SOURCE_FALLBACK')
    demo_data_path: str = Field(default='backend/sample_data/warehouse_stockout_demo.json', alias='DEMO_DATA_PATH')

    lens_api_url: str = Field(default='https://api.lens.org/patent/search', alias='LENS_API_URL')
    lens_api_token: str | None = Field(default=None, alias='LENS_API_TOKEN')

    patent_request_timeout_seconds: int = Field(default=20, alias='PATENT_REQUEST_TIMEOUT_SECONDS')
    patent_cache_ttl_seconds: int = Field(default=900, alias='PATENT_CACHE_TTL_SECONDS')
    patent_cache_maxsize: int = Field(default=512, alias='PATENT_CACHE_MAXSIZE')

    cpc_seed_patents: int = Field(default=5, alias='CPC_SEED_PATENTS')
    cpc_max_codes: int = Field(default=5, alias='CPC_MAX_CODES')
    cpc_second_pass_limit: int = Field(default=10, alias='CPC_SECOND_PASS_LIMIT')

    google_patents_base_url: str = Field(default='https://patents.google.com', alias='GOOGLE_PATENTS_BASE_URL')
    google_patents_timeout_seconds: int = Field(default=10, alias='GOOGLE_PATENTS_TIMEOUT_SECONDS')

    reports_dir: str = Field(default='/tmp/innovation_reports', alias='REPORTS_DIR')
    public_api_base_url: str = Field(default='http://localhost:8000', alias='PUBLIC_API_BASE_URL')

    @property
    def is_lite(self) -> bool:
        return self.app_edition.lower() == 'lite'


@lru_cache(maxsize=1)
def get_settings() -> Settings:
    return Settings()


settings = get_settings()
