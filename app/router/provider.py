from fastapi import APIRouter, Depends
from fastapi.encoders import jsonable_encoder
from starlette.responses import JSONResponse

from common.enums.provider_enum import ProviderGroupType
from core.dependencies import get_provider_service

router = APIRouter()


@router.get("/set-provider")
async def set_provider_data(
        provider_service=Depends(get_provider_service)
):
    result = await provider_service.set_provider_data()
    return JSONResponse(content=jsonable_encoder(result), status_code=200)


@router.get("/provider")
async def get_provider_list(
        provider_type: ProviderGroupType,
        provider_service=Depends(get_provider_service)
):
    result = provider_service.get_provider_list(provider_type)
    return JSONResponse(content=jsonable_encoder(result), status_code=200)
