from fastapi import APIRouter
from sqlalchemy import text

from app.database import engine

router = APIRouter(
    prefix="/api/v1/seasons",
    tags=["Seasons"]
)


@router.get("/highest-scoring")
def get_highest_scoring_seasons(limit: int = 10):

    query = text("""
        SELECT
            season_year,
            matches_played,
            total_runs,
            avg_runs_per_match
        FROM mart_team_seasons
        ORDER BY total_runs DESC
        LIMIT :limit
    """)

    with engine.connect() as conn:
        rows = conn.execute(
            query,
            {"limit": limit}
        ).mappings().all()

    return [dict(row) for row in rows]


@router.get("/run-trends")
def get_run_trends():

    query = text("""
        SELECT
            season_year,
            matches_played,
            total_runs,
            avg_runs_per_match
        FROM mart_team_seasons
        ORDER BY season_year
    """)

    with engine.connect() as conn:
        rows = conn.execute(query).mappings().all()

    return [dict(row) for row in rows]


@router.get("/{season_year}")
def get_season_summary(season_year: int):

    query = text("""
        SELECT
            season_year,
            matches_played,
            total_runs,
            avg_runs_per_match
        FROM mart_team_seasons
        WHERE season_year = :season_year
    """)

    with engine.connect() as conn:
        row = conn.execute(
            query,
            {"season_year": season_year}
        ).mappings().first()

    if row is None:
        return {
            "message": "Season not found"
        }

    return dict(row)