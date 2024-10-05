from sqlalchemy import Column, ForeignKey, Integer, String, Float, Date, Table
from sqlalchemy.orm import relationship
from database import Base

# Many-to-Many relationship tables
movie_languages = Table('movie_languages', Base.metadata,
    Column('movie_id', Integer, ForeignKey('movies.id')),
    Column('language_id', Integer, ForeignKey('languages.id'))
)

movie_genres = Table('movie_genres', Base.metadata,
    Column('movie_id', Integer, ForeignKey('movies.id')),
    Column('genre_id', Integer, ForeignKey('genres.id'))
)

movie_production_companies = Table('movie_production_companies', Base.metadata,
    Column('movie_id', Integer, ForeignKey('movies.id')),
    Column('production_company_id', Integer, ForeignKey('production_companies.id'))
)

class Movie(Base):
    __tablename__ = "movies"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, index=True)
    original_title = Column(String)
    budget = Column(Integer)
    revenue = Column(Integer)
    runtime = Column(Integer)
    release_date = Column(Date, index=True)
    status = Column(String)
    vote_average = Column(Float, index=True)
    vote_count = Column(Integer)
    overview = Column(String)
    homepage = Column(String)

    languages = relationship("Language", secondary=movie_languages, back_populates="movies")
    genres = relationship("Genre", secondary=movie_genres, back_populates="movies")
    production_companies = relationship("ProductionCompany", secondary=movie_production_companies, back_populates="movies")

class Language(Base):
    __tablename__ = "languages"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, unique=True, index=True)

    movies = relationship("Movie", secondary=movie_languages, back_populates="languages")

class Genre(Base):
    __tablename__ = "genres"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, unique=True, index=True)

    movies = relationship("Movie", secondary=movie_genres, back_populates="genres")

class ProductionCompany(Base):
    __tablename__ = "production_companies"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, unique=True, index=True)

    movies = relationship("Movie", secondary=movie_production_companies, back_populates="production_companies")