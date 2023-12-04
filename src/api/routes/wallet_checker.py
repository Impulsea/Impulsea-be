from fastapi import APIRouter, Depends, Query, HTTPException

from api.dependencies import get_activity_wallet_checker_service
from services.activities import Activities
from exceptions.exceptions import (
    ActivityNotExistError,
    EmptyQueryResultError,
    FailedQueryError,
)


router = APIRouter(
    tags=["Activity"]
)


@router.get("/activity_wallet_checker")
async def get_wallet_checker(
    activity: str = Query(...),
    address: str = Query(...),
    get_activity_wallet_checker_service: Activities = Depends(get_activity_wallet_checker_service)
):
    try:
        return get_activity_wallet_checker_service.get_activity_wallet_score(activity, address)
    except ActivityNotExistError as err:
        raise HTTPException(status_code=err.error_code(), detail=str(err))
    except FailedQueryError as err:
        raise HTTPException(status_code=err.error_code(), detail=str(err))
    except EmptyQueryResultError as err:
        raise HTTPException(status_code=err.error_code(), detail=str(err))
