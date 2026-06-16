from fastapi import APIRouter

router = APIRouter(
    prefix="/api/v1/matchups",
    tags=["Matchups"]
)


@router.get("/{batter_id}/{bowler_id}")
def get_matchup(batter_id: str, bowler_id: str):
    return {
        "batter_id": batter_id,
        "bowler_id": bowler_id,
        "message": "matchup endpoint placeholder"
    }