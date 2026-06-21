from fastapi import APIRouter
from sqlalchemy import text

from app.database import engine

router = APIRouter(
    prefix="/api/v1/bowlers",
    tags=["Bowlers"]
)


@router.get("/top-wickets")
def get_top_wicket_takers(limit: int = 10):

    query = text("""
        SELECT
            p.player_name,
            SUM(b.wickets) AS total_wickets,
            COUNT(*) AS spells_bowled,
            ROUND(AVG(b.economy), 2) AS average_economy

        FROM fact_bowling_spells b

        JOIN dim_player p
            ON p.player_sk = b.bowler_sk

        GROUP BY p.player_name

        ORDER BY total_wickets DESC

        LIMIT :limit
    """)

    with engine.connect() as conn:

        rows = conn.execute(
            query,
            {"limit": limit}
        ).mappings().all()

    return [dict(row) for row in rows]


@router.get("/best-economy")
def get_best_economy_bowlers(
    min_spells: int = 50,
    limit: int = 10
):

    query = text("""
        SELECT
            p.player_name,
            COUNT(*) AS spells_bowled,
            SUM(b.wickets) AS wickets,
            ROUND(AVG(b.economy), 2) AS economy

        FROM fact_bowling_spells b

        JOIN dim_player p
            ON p.player_sk = b.bowler_sk

        GROUP BY p.player_name

        HAVING COUNT(*) >= :min_spells

        ORDER BY economy ASC

        LIMIT :limit
    """)

    with engine.connect() as conn:

        rows = conn.execute(
            query,
            {
                "min_spells": min_spells,
                "limit": limit
            }
        ).mappings().all()

    return [dict(row) for row in rows]