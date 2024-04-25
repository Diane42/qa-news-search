from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    # API Setting
    API_HOST: str
    API_PORT: int
    API_WORKERS: int
    API_THREADS: int

    # ELASTICSEARCH
    ES_URL: str
    ES_HOST: str
    ES_USER: str
    ES_PASSWORD: str

    # INDEX
    NEWS_INDEX_NAME: str
    PROVIDER_INDEX_NAME: str

    # FILE PATH
    NEWS_INDEX_JSON: str
    NEWS_INDEX_CSV: str
    PROVIDER_INDEX_JSON: str
    PROVIDER_INDEX_CSV: str

    class Config:
        env_file = "config/.env"
        env_file_encoding = "utf-8"


settings = Settings()
