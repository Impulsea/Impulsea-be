from services.healthcheck import HealthCheck
from services.activities import Activities
from services.db.address import DBAddressService
from services.db.leaderboard import DBLeaderboardService
from db.session import session_maker


def healthcheck() -> HealthCheck:
    return HealthCheck()


def get_activities_service() -> Activities:

    session = session_maker()
    db_address_service = DBAddressService(session)
    db_leaderboard_service = DBLeaderboardService(session)

    return Activities(
        db_address_service=db_address_service,
        db_leaderboard_service=db_leaderboard_service
    )
