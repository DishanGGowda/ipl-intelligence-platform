from fastapi import APIRouter

router = APIRouter(
    prefix="/api/v1/venues",
    tags=["Venues"]
)


@router.get("/{venue_id}/analysis")
def get_venue_analysis(venue_id: str):
    return {
        "venue_id": venue_id,
        "message": "venue analysis endpoint placeholder"
    }