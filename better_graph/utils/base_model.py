import typing

from bson.objectid import ObjectId
from pydantic import BaseModel, Field, validator

from better_graph.utils.check_type import check_instance


class BaseModel_(BaseModel):
    def dict_(self):
        d: dict = self.dict()
        if d.get('id'):
            d['_id'] = d.pop('id')
        if not d.get('id', '__IMPOSSIBLE_TOKEN__') == '__IMPOSSIBLE_TOKEN__':
            d.pop('id')
        return d

    @validator('id', check_fields=False)
    def validate_id(cls, v):
        if isinstance(v, str):
            return ObjectId(v)
        check_instance(v, ObjectId)
        return ObjectId


class InputModel(BaseModel_):
    id: typing.Optional[str] = Field(alias='id')


class OutputModel(BaseModel_):
    id: typing.Optional[str] = Field(alias='_id')
