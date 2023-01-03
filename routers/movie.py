from typing import List

from fastapi import APIRouter
from fastapi import Path, Query, status, Depends
from fastapi.encoders import jsonable_encoder
from starlette.responses import JSONResponse

from config.database import Session
from middlewares.jwt_bearer import JWTBearer
from models.movie import Movie as MovieModel
from schemas.movie import Movie
from services.movie import MovieService

movie_router = APIRouter()


@movie_router.get('/movies', tags=['movies'],
                  response_model=List[Movie],
                  status_code=status.HTTP_200_OK,
                  dependencies=[Depends(JWTBearer())])
def get_movies() -> JSONResponse:
    db = Session()
    result = MovieService(db).get_movies()
    return JSONResponse(content=jsonable_encoder(result))


@movie_router.get('/movies/{id}', tags=['movies'], response_model=Movie, status_code=status.HTTP_200_OK)
def get_movies(id: int = Path(ge=1, le=2000)) -> JSONResponse:
    db = Session()
    result = MovieService(db).get_movie(id)
    if not result:
        return JSONResponse(status_code=status.HTTP_404_NOT_FOUND, content={"message": "Movie not found"})
    return JSONResponse(status_code=status.HTTP_200_OK, content=jsonable_encoder(result))


@movie_router.get('/movies/', tags=['movies'], response_model=List[Movie], status_code=status.HTTP_200_OK)
def get_movies_by_category(categorys: str = Query(min_length=5, max_length=15)) -> JSONResponse:
    db = Session()
    result = MovieService(db).get_category(categorys)
    if not result:
        return JSONResponse(status_code=status.HTTP_404_NOT_FOUND, content={"message": "Category not found"})
    return JSONResponse(status_code=status.HTTP_200_OK, content=jsonable_encoder(result))


@movie_router.post('/movies', tags=['movies'],
                   response_model=List[Movie],
                   status_code=status.HTTP_201_CREATED)
def create_movie(movie: Movie) -> JSONResponse:
    db = Session()
    MovieService(db).create_movie(movie)
    return JSONResponse(content="Se ha registrado una pelicula")


@movie_router.delete('/movies/{id}', tags=['movies'], response_model=dict, status_code=status.HTTP_200_OK)
def delete_movie(id: int) -> JSONResponse:
    db = Session()
    result = MovieService(db).get_movie(id)
    if not result:
        return JSONResponse(status_code=status.HTTP_404_NOT_FOUND, content={"message": "dont exist the movie"})
    MovieService(db).delete_movie(id)
    MovieService(db).delete_movie(id)
    return JSONResponse(content={"message": "the movie is deleted"}, status_code=status.HTTP_200_OK)


@movie_router.put('/movies/{id}', tags=['movies'], response_model=dict, status_code=status.HTTP_200_OK)
def edit_movie(id: int,
               movie: Movie) -> JSONResponse:
    db = Session()
    result = MovieService(db).get_movie(id)
    if not result:
        return JSONResponse(status_code=status.HTTP_404_NOT_FOUND, content={"message": "dont exist the movie"})
    MovieService(db).update_movie(id, movie)
    return JSONResponse(content={"message": "the movie is updated"})
