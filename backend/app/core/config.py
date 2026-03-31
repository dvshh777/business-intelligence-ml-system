from functools import lru_cache
from pathlib import Path

from pydantic import field_validator
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    app_name: str = "Business Intelligence ML API"
    app_env: str = "development"
    api_v1_prefix: str = "/api/v1"
    database_url: str = "postgresql+psycopg://bi_user:bi_password@localhost:5432/bi_ml"
    model_path: str = "../artifacts/churn_model.joblib"
    metrics_path: str = "../artifacts/model_metrics.json"
    cors_origins: list[str] = ["http://localhost:5173"]

    model_config = SettingsConfigDict(env_file=".env", env_file_encoding="utf-8")

    @field_validator("cors_origins", mode="before")
    @classmethod
    def split_cors_origins(cls, value: str | list[str]) -> list[str]:
        if isinstance(value, str):
            return [item.strip() for item in value.split(",") if item.strip()]
        return value

    @property
    def resolved_model_path(self) -> Path:
        return (Path(__file__).resolve().parents[3] / self.model_path).resolve()

    @property
    def resolved_metrics_path(self) -> Path:
        return (Path(__file__).resolve().parents[3] / self.metrics_path).resolve()


@lru_cache
def get_settings() -> Settings:
    return Settings()
