from fastapi import APIRouter, Depends, Query

from api.dependencies import get_activity_wallet_checker_service
from services.activities import Activities


router = APIRouter(
    tags=["LB"]
)


@router.get("/activity_wallet_checker")
async def wallet_checker(
    activity: str = Query(...),
    address: str = Query(...),
    get_activity_wallet_checker_service: Activities = Depends(get_activity_wallet_checker_service)
):
    return get_activity_wallet_checker_service.get_activity_wallet_score(activity, address)
