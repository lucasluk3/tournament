from fastapi import FastAPI

from core.api.v1.tournament import router as tournament_router

app = FastAPI()

app.include_router(tournament_router)


