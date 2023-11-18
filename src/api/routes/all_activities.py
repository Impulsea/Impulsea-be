from fastapi import APIRouter, Depends, Query

from api.dependencies import get_all_activities_service
from services.activities import Activities


router = APIRouter(
    tags=["All"]
)


@router.get("/all_activities")
async def all_activities(
    all_ativities_service: Activities = Depends(get_all_activities_service)
):
    return all_ativities_service.get_all_activities()
