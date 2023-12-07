from fastapi import APIRouter, Depends

from api.dependencies import get_activities_service
from services.activities import Activities


router = APIRouter(
    tags=["All activities"]
)


@router.get("/all_activities")
async def get_all_activities(
    all_ativities_service: Activities = Depends(get_activities_service)
):
    return all_ativities_service.get_all_activities()
