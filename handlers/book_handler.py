from fastapi import APIRouter
from dto.book import Book


router = APIRouter(
    prefix="/api/v1/books",
    tags=["books"]
)


@router.get('/author/{author_id}', response_model=Book, summary='asdasd')
async def get_books_by_author(author_id: int):
    return Book(id="1314", name="asdasd").dict()


@router.get('/author/{book_id}')
async def get_book(book_id: int):
    pass


@router.get('/download/{book_id}')
async def download_book(book_id: int):
    pass


@router.get('/by_name/{name}')
async def get_book_by_name(name: str):
    pass


@router.get('/genre/{genre_id}')
async def get_books_by_genre(genre_id: int):
    pass


@router.get('/popular')
async def get_popular_books():
    pass


@router.get('/search/')
async def search_book():
    pass
