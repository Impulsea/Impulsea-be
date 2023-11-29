from fastapi import APIRouter, Depends, Query, HTTPException

from api.dependencies import get_activity_stats_service
from services.activities import Activities
from exceptions.exceptions import ActivityNotExistError


router = APIRouter(
    tags=["Activity"]
)


@router.get("/activity_stats")
async def get_activity_stats(
    activity: str = Query(...),
    ativitity_stats_service: Activities = Depends(get_activity_stats_service)
):
    try:
        return ativitity_stats_service.get_activity_stats(activity)
    except ActivityNotExistError as err:
        raise HTTPException(status_code=err.error_code(), detail=str(err))
