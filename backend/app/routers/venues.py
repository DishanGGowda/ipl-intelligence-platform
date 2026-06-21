from fastapi import APIRouter
from sqlalchemy import text

from app.database import engine

router = APIRouter(
    prefix="/api/v1/venues",
    tags=["Venues"]
)


@router.get("/highest-scoring")
def get_highest_scoring_venues(limit: int = 10):

    query = text("""
        SELECT
            v.venue_name,
            v.city,

            COUNT(DISTINCT m.match_sk) AS matches_played,

            SUM(fd.runs_total) AS total_runs,

            ROUND(
                SUM(fd.runs_total) * 1.0
                / COUNT(DISTINCT m.match_sk),
                2
            ) AS avg_runs_per_match

        FROM fact_deliveries fd

        JOIN dim_match m
            ON m.match_sk = fd.match_sk

        JOIN dim_venue v
            ON v.venue_sk = m.venue_id

        GROUP BY
            v.venue_name,
            v.city

        HAVING COUNT(DISTINCT m.match_sk) >= 10

        ORDER BY avg_runs_per_match DESC

        LIMIT :limit
    """)

    with engine.connect() as conn:

        rows = conn.execute(
            query,
            {"limit": limit}
        ).mappings().all()

    return [dict(row) for row in rows]