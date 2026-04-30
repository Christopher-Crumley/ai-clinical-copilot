from pathlib import Path
from pydantic_settings import BaseSettings

ROOT_DIR = Path(__file__).resolve().parents[3]


class Settings(BaseSettings):
    openai_api_key: str
    pinecone_api_key: str
    pinecone_index_name: str = "clinical-copilot"
    pinecone_environment: str = "gcp-starter"
    model_name: str = "gpt-4o"
    embedding_model: str = "text-embedding-3-small"
    chunk_size: int = 500
    chunk_overlap: int = 75
    top_k: int = 5
    allowed_origins: str = "http://localhost:3000"

    model_config = {
        "env_file": str(ROOT_DIR / ".env"),
        "protected_namespaces": (),
        "extra": "ignore",
    }


settings = Settings()
