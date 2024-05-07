import uvicorn

from core.config import settings

if __name__ == "__main__":
    uvicorn.run("core.app:news_app", host=settings.API_HOST, port=settings.API_PORT, reload=True)