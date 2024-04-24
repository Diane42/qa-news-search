from app.repository.news_repository import NewsRepository


class NewsService:
    def __init__(self, news_repository: NewsRepository):
        self.news_repository = news_repository

