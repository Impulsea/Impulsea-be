from fastapi import APIRouter, Depends, Query, HTTPException

from api.dependencies import get_activities_service
from services.activities import Activities
from exceptions.exceptions import ActivityNotExistError

router = APIRouter(
    tags=["Activity"]
)


@router.get("/leaderboard")
async def get_leaderbaord(
    activity: str = Query(...),
    activity_leaderboard_service: Activities = Depends(get_activities_service)
):
    try:
        return activity_leaderboard_service.get_activity_leaderboard(activity)
    except ActivityNotExistError as err:
        raise HTTPException(status_code=err.error_code(), detail=str(err))
