from fastapi import APIRouter, HTTPException
from sqlalchemy import text

from app.database import engine

router = APIRouter(
    prefix="/api/v1/matchups",
    tags=["Matchups"]
)


@router.get("/top-rivalries/list")
def get_top_rivalries(limit: int = 20):

    query = text("""
        SELECT
            batter.player_name AS batter_name,
            bowler.player_name AS bowler_name,
            m.runs_scored,
            m.balls_faced,
            m.dismissals,

            ROUND(
                (m.runs_scored * 100.0)
                / NULLIF(m.balls_faced, 0),
                2
            ) AS strike_rate

        FROM fact_player_matchups m

        JOIN dim_player batter
            ON batter.player_sk = m.batter_sk

        JOIN dim_player bowler
            ON bowler.player_sk = m.bowler_sk

        ORDER BY m.balls_faced DESC

        LIMIT :limit
    """)

    with engine.connect() as conn:

        rows = conn.execute(
            query,
            {
                "limit": limit
            }
        ).mappings().all()

    return [dict(row) for row in rows]


@router.get("/{batter_name}/{bowler_name}")
def get_matchup(
    batter_name: str,
    bowler_name: str
):

    query = text("""
        SELECT
            batter.player_name AS batter_name,
            bowler.player_name AS bowler_name,
            m.runs_scored,
            m.balls_faced,
            m.dismissals,

            ROUND(
                (m.runs_scored * 100.0)
                / NULLIF(m.balls_faced, 0),
                2
            ) AS strike_rate

        FROM fact_player_matchups m

        JOIN dim_player batter
            ON batter.player_sk = m.batter_sk

        JOIN dim_player bowler
            ON bowler.player_sk = m.bowler_sk

        WHERE lower(batter.player_name)
              = lower(:batter_name)

        AND lower(bowler.player_name)
              = lower(:bowler_name)
    """)

    with engine.connect() as conn:

        row = conn.execute(
            query,
            {
                "batter_name": batter_name,
                "bowler_name": bowler_name
            }
        ).mappings().first()

    if not row:
        raise HTTPException(
            status_code=404,
            detail="Matchup not found"
        )

    return dict(row)