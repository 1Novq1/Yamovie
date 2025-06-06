from typing import List

from .data_manager_interface import DataManagerInterface
from .data_models import Movie


class Movies:

    def __init__(self, data_manager: DataManagerInterface):
        self._data_manager = data_manager

    @staticmethod
    def __movie_to_dict(movie) -> dict:
        movie_reviews = []
        if movie.movie_reviews:
            for review in movie.movie_reviews:
                movie_reviews.append({
                    "id": review.id,
                    "user_id": review.user_id,
                    "movie_id": review.movie_id,
                    "review_text": review.review_text,
                    "rating": review.rating,
                    "user": {"user_id": review.user.id,
                             "user_name": review.user.user_name }
                })

        return {"id": movie.id,
                "movie_name": movie.movie_name,
                "director": movie.director,
                "year": movie.year,
                "rating": movie.rating,
                "poster": movie.poster,
                "website": movie.website,
                "movie_reviews": movie_reviews
                }

    def get_movies(self) -> List[dict] | None:
        movies_query = self._data_manager.get_all_data()
        if movies_query is None:
            return None

        movies = []
        for movie in movies_query:
            movies.append(self.__movie_to_dict(movie))
        return movies

    def get_movie(self, movie_id: int) -> dict | None:
        movie = self._data_manager.get_item_by_id(movie_id)
        if not movie:
            return None
        return self.__movie_to_dict(movie)

    @staticmethod
    def __instantiate_new_movie(new_movie_info):
        return Movie(
            movie_name=new_movie_info['movie_name'],
            director=new_movie_info['director'],
            year=new_movie_info['year'],
            rating=new_movie_info['rating'],
            poster=new_movie_info['poster'],
            website=new_movie_info['website']
        )

    def add_new_movie(self, new_movie_info: dict) -> bool | None:
        return self._data_manager.add_item(self.__instantiate_new_movie(new_movie_info))

    def update_movie(self, updated_movie: dict):
        return self._data_manager.update_item(updated_movie)

    def delete_movie(self, movie_id: int) -> bool | None:
        return self._data_manager.delete_item(movie_id)
