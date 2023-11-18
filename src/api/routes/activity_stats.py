from fastapi import APIRouter, Depends, Query

from api.dependencies import get_activity_stats_service
from services.activities import Activities


router = APIRouter(
    tags=["Activity"]
)


@router.get("/activity_stats")
async def activity_stats(
    activity: str = Query(...),
    ativitity_stats_service: Activities = Depends(get_activity_stats_service)
):
    return ativitity_stats_service.get_activity_stats(activity)
