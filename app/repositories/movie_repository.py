from sqlalchemy.orm import Session
from models import Movie, Language, Genre, ProductionCompany
from datetime import datetime
from typing import Optional

class MovieRepository:
    def __init__(self, db: Session):
        self.db = db

    def create_movie(self, movie_data: dict):
        # Convert release_date string to a date object
        try:
            release_date = datetime.strptime(movie_data['release_date'], '%Y-%m-%d').date()
        except ValueError:
            release_date = None  # Handle invalid date formats or missing dates gracefully

        # Create or get existing Language, Genre, and ProductionCompany instances
        language = self.get_or_create(Language, name=movie_data['original_language'])
        genre = self.get_or_create(Genre, name=movie_data['genre_id'])
        production_company = self.get_or_create(ProductionCompany, name=movie_data['production_company_id'])

        # Create Movie instance with the correct release_date
        movie = Movie(
            title=movie_data['title'],
            original_title=movie_data['original_title'],
            budget=movie_data['budget'],
            revenue=movie_data['revenue'],
            runtime=movie_data['runtime'],
            release_date=release_date,  # Insert date object here
            status=movie_data['status'],
            vote_average=movie_data['vote_average'],
            vote_count=movie_data['vote_count'],
            overview=movie_data['overview'],
            homepage=movie_data['homepage']
        )

        # Associate related entities
        movie.languages.append(language)
        movie.genres.append(genre)
        movie.production_companies.append(production_company)

        self.db.add(movie)
        self.db.commit()
        self.db.refresh(movie)
        return movie

    def get_or_create(self, model, **kwargs):
        instance = self.db.query(model).filter_by(**kwargs).first()
        if instance:
            return instance
        else:
            instance = model(**kwargs)
            self.db.add(instance)
            self.db.commit()
            return instance
        
    def get_movies(self, page: int, per_page: int, year: Optional[int], language: Optional[str], sort_by: str, sort_order: str):
        query = self.db.query(Movie)
        
        # Filtering by year of release
        if year:
            query = query.filter(Movie.release_date.like(f'{year}%'))
        
        # Filtering by language
        if language:
            query = query.join(Movie.languages).filter(Language.name == language)
        
        # Sorting by release_date or vote_average
        if sort_by == 'release_date':
            if sort_order == 'asc':
                query = query.order_by(Movie.release_date.asc())
            else:
                query = query.order_by(Movie.release_date.desc())
        elif sort_by == 'vote_average':
            if sort_order == 'asc':
                query = query.order_by(Movie.vote_average.asc())
            else:
                query = query.order_by(Movie.vote_average.desc())

        # Pagination
        offset = (page - 1) * per_page
        query = query.offset(offset).limit(per_page)

        return query.all()
