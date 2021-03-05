from fastapi import APIRouter


router = APIRouter(
    prefix="/api/v1/genres",
    tags=["genres"]
)


@router.get('/')
def get_all_genres():
    pass
