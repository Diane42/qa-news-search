from core.config import settings

bind = f"{settings.API_HOST}:{settings.API_PORT}"
workers = f"{settings.API_WORKERS}"
wsgi_app = "core.app:news_app"
worker_class = "uvicorn.workers.UvicornWorker"
accesslog = "-"
timeout = 60
