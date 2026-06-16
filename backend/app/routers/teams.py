from fastapi import APIRouter

router = APIRouter(
    prefix="/api/v1/teams",
    tags=["Teams"]
)


@router.get("/{team_id}/stats")
def get_team_stats(team_id: str):
    return {
        "team_id": team_id,
        "message": "team stats endpoint placeholder"
    }