from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    # API Setting
    API_HOST: str
    API_PORT: int
    API_WORKERS: int
    API_THREADS: int

    class Config:
        env_file = "config/.env"
        env_file_encoding = "utf-8"


settings = Settings()
