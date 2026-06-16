from fastapi import APIRouter

router = APIRouter(
    prefix="/api/v1/players",
    tags=["Players"]
)


@router.get("/{player_id}/career")
def get_player_career(player_id: str):
    return {
        "player_id": player_id,
        "message": "career endpoint placeholder"
    }