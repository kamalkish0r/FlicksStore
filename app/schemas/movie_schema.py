from datetime import date
from pydantic import BaseModel
from typing import List, Optional

class LanguageSchema(BaseModel):
    id: int
    name: str

    class Config:
        orm_mode = True  # Needed for compatibility with SQLAlchemy models

class GenreSchema(BaseModel):
    id: int
    name: str

    class Config:
        orm_mode = True

class ProductionCompanySchema(BaseModel):
    id: int
    name: str

    class Config:
        orm_mode = True

class MovieSchema(BaseModel):
    id: int
    title: str
    original_title: Optional[str]
    budget: Optional[int]
    revenue: Optional[int]
    runtime: Optional[int]
    release_date: Optional[date]
    status: Optional[str]
    vote_average: Optional[float]
    vote_count: Optional[int]
    overview: Optional[str]
    homepage: Optional[str]

    languages: List[LanguageSchema]
    genres: List[GenreSchema]
    production_companies: List[ProductionCompanySchema]

    class Config:
        orm_mode = True
