from fastapi import FastAPI

from app.routers import players
from app.routers import venues
from app.routers import matchups
from app.routers import bowlers
from app.routers import seasons

app = FastAPI(
    title="IPL Intelligence Platform API",
    version="1.0.0",
    description="IPL Cricket Intelligence Platform"
)

# =========================
# ROUTERS
# =========================

app.include_router(players.router)
app.include_router(venues.router)
app.include_router(matchups.router)
app.include_router(bowlers.router)
app.include_router(seasons.router)

# =========================
# HEALTH CHECK
# =========================

@app.get("/")
def root():

    return {
        "status": "healthy",
        "service": "ipl-intelligence-platform",
        "version": "1.0.0"
    }