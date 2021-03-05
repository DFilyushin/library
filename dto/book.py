from typing import Optional
from pydantic import BaseModel


class Book(BaseModel):
    id: str
    name: Optional[str]
    authors: Optional[str]
    series: Optional[str]
    sernum: Optional[str]
    filename: Optional[str]
    deleted: Optional[str]
    lang: Optional[str]
    keywords: Optional[str]
    added: Optional[str]
    genres: Optional[str]
    year: Optional[str]
    isbn: Optional[str]
    city: Optional[str]
    pub_name: Optional[str]
    publisher: Optional[str]
    height: Optional[str]
    width: Optional[str]