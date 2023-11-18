from fastapi import FastAPI

from api.routes import setup_routes


def create_app() -> FastAPI:
    app = FastAPI()
    setup_routes(app)
    return app


app = create_app()
