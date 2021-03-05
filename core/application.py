from fastapi import FastAPI
from handlers.book_handler import router as book_router
from handlers.author_handler import router as author_router
from handlers.genre_handler import router as genre_handler
from handlers.user_handler import router as user_handler


class Application(FastAPI):
    def __init__(self):
        super().__init__(title='My API')
        self.init_routes()

    def init_routes(self):
        self.include_router(book_router)
        self.include_router(author_router)
        self.include_router(genre_handler)
        self.include_router(user_handler)
