from fastapi import APIRouter
from dto.author import Author


router = APIRouter(
    prefix="/api/v1/authors",
    tags=["authors"]
)


@router.get('/all', summary='Get all authors')
async def get_all_authors():
    pass


@router.get('/{author_id}', summary='Get author by author_id')
async def get_author_by_id(author_id: int):
    pass


@router.get('/start_with/{start_text_fullname}', summary='Find authors by start string')
async def get_authors_startwith(start_text_fullname):
    pass


@router.get('/{author_id}/genres', summary='Get author genres by author_id')
def get_author_genres(author_id: int):
    pass