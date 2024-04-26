from fastapi import Request

from app.service.news_service import NewsService
from app.service.provider_service import ProviderService


def get_news_service(req: Request) -> NewsService:
    return req.app.container.NewsService()


def get_provider_service(req: Request) -> ProviderService:
    return req.app.container.ProviderService()
