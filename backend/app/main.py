from fastapi import FastAPI

from backend.app.routers import players
from backend.app.routers import teams
from backend.app.routers import venues
from backend.app.routers import matchups

app = FastAPI(
    title="IPL Intelligence Platform API",
    version="1.0.0",
    description="IPL Cricket Intelligence Platform"
)

app.include_router(players.router)
app.include_router(teams.router)
app.include_router(venues.router)
app.include_router(matchups.router)


@app.get("/")
def root():
    return {
        "status": "healthy",
        "service": "ipl-intelligence-platform"
    }