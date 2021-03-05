from typing import List
from pydantic import BaseSettings
from pathlib import Path

base_dir = Path(__file__).parent.parent.parent.absolute()


class Settings(BaseSettings):
    title_application: str

    library_index: str
    library_zip: str
    library_coverage: str
    temp_dir: str

    mongo_host: str
    mongo_port: str
    mongo_db: str

    redis_host: str
    redis_port: str
    redis_db: str

    use_sessions: bool

    cache_four_week: int

    result_limit: int
    result_skip: int

    book_format: List[str]
    book_thumbnail_height: int
    book_thumbnail_weight: int

    class Config:
        env_file = f'{base_dir}/.env'
