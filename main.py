from __future__ import annotations
from enum import Enum
from typing import List, Optional, Union, Any

from fastapi.encoders import jsonable_encoder
from pydantic import BaseModel, Field
from fastapi import FastAPI
from starlette import status
from starlette.responses import JSONResponse

app = FastAPI()


class ValidationError(BaseModel):
    loc: List[Union[str, int]] = Field(..., title='Location')
    msg: str = Field(..., title='Message')
    type: str = Field(..., title='Error Type')


class HTTPValidationError(BaseModel):
    detail: Optional[List[ValidationError]] = Field(None, title='Detail')


class DogType(str, Enum):
    terrier = "terrier"
    bulldog = "bulldog"
    dalmatian = "dalmatian"


class Dog(BaseModel):
    name: str
    pk: int
    kind: DogType


def dog_kind(dog:Dog):
    return dog.kind
class Timestamp(BaseModel):
    id: int
    timestamp: int


dogs_db = {
    0: Dog(name='Bob', pk=0, kind='terrier'),
    1: Dog(name='Marli', pk=1, kind="bulldog"),
    2: Dog(name='Snoopy', pk=2, kind='dalmatian'),
    3: Dog(name='Rex', pk=3, kind='dalmatian'),
    4: Dog(name='Pongo', pk=4, kind='dalmatian'),
    5: Dog(name='Tillman', pk=5, kind='bulldog'),
    6: Dog(name='Uga', pk=6, kind='bulldog')
}

post_db = [
    Timestamp(id=0, timestamp=12),
    Timestamp(id=1, timestamp=10)
]

@app.get(
    '/dog', response_model=List[Dog], responses={'422': {'model': HTTPValidationError}}
)
def get_dogs_dog_get(
        kind: Optional[DogType] = None,
) -> JSONResponse:
    return JSONResponse(
        status_code=status.HTTP_200_OK,
        content=jsonable_encoder(
            dogs_db
        ))


@app.post('/dog', response_model=Dog, responses={'422': {'model': HTTPValidationError}})
def create_dog_dog_post(body: Dog) -> JSONResponse:
    key = dogs_db.__len__()
    dogs_db[key+1] = body
    return JSONResponse(
        status_code=status.HTTP_200_OK,
        content=jsonable_encoder(
         body
        ))



@app.get(
    '/dog/{pk}', response_model=Dog, responses={'422': {'model': HTTPValidationError}}
)
def get_dog_by_pk_dog__pk__get(pk: int) -> Union[Dog, HTTPValidationError]:
    return dogs_db[pk]

@app.get(
    '/dog/type/{kind}', response_model=List[Dog], responses={'422': {'model': HTTPValidationError}}
)
def get_dogs_by_type(kind: str) -> JSONResponse:
    filtered = []
    for dog in dogs_db.values():
        if dog.kind == kind:
            filtered.append(dog)
    return JSONResponse(
        status_code=status.HTTP_200_OK,
        content=jsonable_encoder(
         filtered
        ))
@app.patch(
    '/dog/{pk}', response_model=Dog, responses={'422': {'model': HTTPValidationError}}
)
def update_dog_dog__pk__patch(
        pk: int, body: Dog
) -> Union[Dog, HTTPValidationError]:
    dogs_db[pk] = body
    return JSONResponse(
        status_code=status.HTTP_200_OK,
        content=jsonable_encoder(
         dogs_db
        ))


@app.post('/post', response_model=Timestamp)
def get_post_post_post(body:Timestamp) -> Timestamp:
    post_db.append(body)
    return body


@app.get('/post_all', response_model=Timestamp)
def get_all_posts() -> JSONResponse:
    return JSONResponse(
        status_code=status.HTTP_200_OK,
        content=jsonable_encoder(
         post_db
        ))



@app.get('/')
def root():
    return 'Hello world!'