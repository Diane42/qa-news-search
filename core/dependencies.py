from fastapi import Request

from app.service.news_service import NewsService


def get_news_service(req: Request) -> NewsService:
    return req.app.container.NewsService()
