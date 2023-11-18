from fastapi import APIRouter, Depends

from api.dependencies import healthcheck
from services.healthcheck import HealthCheck


router = APIRouter(
    tags=["Healthcheck"]
)


@router.get("/healthcheck")
async def healthcheck(
    healthCheck_service: HealthCheck = Depends(healthcheck)
):
    return healthCheck_service.healthcheck()
