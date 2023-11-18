from fastapi import FastAPI

from api.routes import (
    healthcheck,
    all_activities,
    leaderboard,
    wallet_checker,
    activity_stats
)


def setup_routes(app: FastAPI) -> None:
    app.include_router(healthcheck.router, prefix="/api")
    app.include_router(all_activities.router, prefix="/api")
    app.include_router(activity_stats.router, prefix="/api")
    app.include_router(leaderboard.router, prefix="/api")
    app.include_router(wallet_checker.router, prefix="/api")
