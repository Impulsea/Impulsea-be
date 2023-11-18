from services.healthcheck import HealthCheck
from services.activities import Activities


def healthcheck() -> HealthCheck:
    return HealthCheck()


def get_all_activities_service() -> Activities:
    return Activities()


def get_activity_leaderboard_service() -> Activities:
    return Activities()


def get_activity_wallet_checker_service() -> Activities:
    return Activities()
