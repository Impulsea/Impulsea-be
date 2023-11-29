from fastapi import APIRouter, Depends, Query

from api.dependencies import get_activity_leaderboard_service
from services.activities import Activities


router = APIRouter(
    tags=["Activity"]
)


@router.get("/leaderboard")
async def get_leaderbaord(
    activity: str = Query(...),
    get_activity_leaderboard_service: Activities = Depends(get_activity_leaderboard_service)
):
    return get_activity_leaderboard_service.get_activity_leaderboard(activity)
