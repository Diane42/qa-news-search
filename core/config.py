from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    # API Setting
    API_HOST: str
    API_PORT: int
    LOG_PATH: str

    # ELASTICSEARCH
    ES_HOST: str

    # INDEX
    NEWS_INDEX_NAME: str
    PROVIDER_INDEX_NAME: str
    CATEGORY_INDEX_NAME: str

    # FILE PATH
    NEWS_INDEX_SETTING: str
    NEWS_INDEX_DATA: str
    PROVIDER_INDEX_SETTING: str
    PROVIDER_INDEX_DATA: str
    CATEGORY_INDEX_SETTING: str
    CATEGORY_INDEX_DATA: str

    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"


settings = Settings()
