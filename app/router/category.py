from fastapi import APIRouter, Depends
from fastapi.encoders import jsonable_encoder
from starlette.responses import JSONResponse

from common.category_enum import CategoryType
from core.dependencies import get_category_service

router = APIRouter()


@router.get("/set-category")
async def set_category_data(
        category_service=Depends(get_category_service)
):
    result = await category_service.set_category_data()
    return JSONResponse(content=jsonable_encoder(result), status_code=200)


@router.get("/category")
async def get_category_list(
        category_type: CategoryType,
        category_service=Depends(get_category_service)
):
    result = category_service.get_category_list(category_type)
    return JSONResponse(content=jsonable_encoder(result), status_code=200)
