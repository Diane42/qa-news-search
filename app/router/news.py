from fastapi import APIRouter, Depends
from fastapi.encoders import jsonable_encoder
from starlette.responses import JSONResponse

from core.dependencies import get_news_service
from app.router.parameters.news_param import get_news_params

router = APIRouter()


@router.get("/set-news-data")
async def set_news_data(
        news_service=Depends(get_news_service)
):
    result = await news_service.set_news_data()
    return JSONResponse(content=jsonable_encoder(result), status_code=200)


@router.get("/news")
async def search_news(
        request=Depends(get_news_params),
        news_service=Depends(get_news_service)
):
    result = news_service.search_news(request)
    return JSONResponse(content=jsonable_encoder(result), status_code=200)
