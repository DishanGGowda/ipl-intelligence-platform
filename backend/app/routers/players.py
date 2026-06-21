from fastapi import APIRouter, HTTPException
from sqlalchemy import text

from app.database import engine

router = APIRouter(
    prefix="/api/v1/players",
    tags=["Players"]
)


@router.get("/{player_name}/career")
def get_player_career(player_name: str):

    query = text("""
        SELECT *
        FROM mart_player_career
        WHERE lower(player_name) = lower(:player_name)
    """)

    with engine.connect() as conn:
        row = conn.execute(
            query,
            {"player_name": player_name}
        ).mappings().first()

    if not row:
        raise HTTPException(
            status_code=404,
            detail="Player not found"
        )

    return dict(row)


@router.get("/top-runs")
def get_top_run_scorers(limit: int = 10):

    query = text("""
        SELECT
            player_name,
            career_runs,
            strike_rate,
            highest_score
        FROM mart_player_career
        ORDER BY career_runs DESC
        LIMIT :limit
    """)

    with engine.connect() as conn:
        rows = conn.execute(
            query,
            {"limit": limit}
        ).mappings().all()

    return [dict(row) for row in rows]


@router.get("/top-strike-rate")
def get_top_strike_rate_batters(
    min_runs: int = 1000,
    limit: int = 10
):

    query = text("""
        SELECT
            player_name,
            career_runs,
            strike_rate,
            highest_score,
            innings_played

        FROM mart_player_career

        WHERE career_runs >= :min_runs

        ORDER BY strike_rate DESC

        LIMIT :limit
    """)

    with engine.connect() as conn:

        rows = conn.execute(
            query,
            {
                "min_runs": min_runs,
                "limit": limit
            }
        ).mappings().all()

    return [dict(row) for row in rows]

@router.get("/{player_name}/season-trend")
def get_player_season_trend(player_name: str):

    query = text("""
        SELECT
            season_year,
            innings_played,
            runs,
            balls,
            fours,
            sixes,
            highest_score,
            strike_rate

        FROM mart_player_seasons

        WHERE lower(player_name) = lower(:player_name)

        ORDER BY season_year
    """)

    with engine.connect() as conn:

        rows = conn.execute(
            query,
            {
                "player_name": player_name
            }
        ).mappings().all()

    if not rows:
        raise HTTPException(
            status_code=404,
            detail="Player not found"
        )

    return [dict(row) for row in rows]