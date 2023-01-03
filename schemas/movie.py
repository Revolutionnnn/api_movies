from typing import Optional

from pydantic import BaseModel, Field


class Movie(BaseModel):
    id: Optional[int] = None
    title: str = Field(default='title of movie', min_length=1, max_length=15)
    overview: str = Field(default='content movie', in_length=15, max_length=100)
    year: int = Field(default=2022, le=2022)
    rating: float = Field(default=5.0, ge=1.0, le=10.0)
    category: str = Field(default='action', min_length=1, max_length=15)

    class config:
        schema_extra = {
            'example': {
                'id': 1,
                'tile': 'title of movie',
                'overview': 'content of movie',
                'year': "2022",
                'rating': 5.0,
                'category': 'action'
            }
        }
