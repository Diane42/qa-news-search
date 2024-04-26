from typing import Optional

from fastapi import APIRouter, Depends
from fastapi.encoders import jsonable_encoder
from starlette.responses import JSONResponse

from common.enums.provider_enum import ProviderType
from core.dependencies import get_provider_service

router = APIRouter()


@router.get("/provider")
async def get_provider(
    provider_type: ProviderType,
    type_name: Optional[str] = None,
    provider_service=Depends(get_provider_service)
):
    result = provider_service.get_provider(provider_type, type_name)
    return JSONResponse(content=jsonable_encoder(result), status_code=200)

