from collections import Iterable

from bson.objectid import ObjectId


class MutationResolver:
    def __init__(
            self,
            name: str,
            base_adapter,
    ):
        self.name = name
        self.base_adapter = base_adapter[name.lower()]

    async def create(self, document) -> Iterable:
        return self.base_adapter.insert_one(document.dict())

    async def update(self, document) -> Iterable:
        if not isinstance(document, dict):
            document = document.dict()
        filter_ = {
            '_id': ObjectId(document.pop('id'))
        }
        update = {
            '$set': {**document}
        }
        return self.base_adapter.update_one(filter_, update)

    async def delete(self, document) -> Iterable:
        filter_ = {
            '_id': ObjectId(document.id)
        }
        return self.base_adapter.delete_one(filter_)
