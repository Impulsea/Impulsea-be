from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from api.routes import setup_routes


def create_app() -> FastAPI:

    app = FastAPI(
        title="Impulsea API",
        docs_url="/"
    )

    app.add_middleware(
        CORSMiddleware,
        allow_origins=["http://localhost:3000", "localhost:3000"],
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"]
    )

    setup_routes(app)

    return app


app = create_app()
