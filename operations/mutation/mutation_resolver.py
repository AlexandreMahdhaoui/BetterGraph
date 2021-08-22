import os

from bson import ObjectId
from pymongo import MongoClient


class MutationResolver:
    def __init__(
            self,
            name: str,
            cnx_str_key: str = "CNX_STR",
            db_name_key: str = "DB_NAME",
    ):
        self.name = name
        cnx_str = os.getenv(cnx_str_key)
        db_name = os.getenv(db_name_key)
        self.db_client: MongoClient = MongoClient(cnx_str)[db_name]['collection_{}'.format(name)]
        del cnx_str, db_name

    async def create(self, document):
        return self.db_client.insert_one(document.dict())

    async def update(self, document):
        doc = document.dict()
        filter_ = {
            '_id': ObjectId(doc.pop('id'))
        }
        update = {
            '$set': {**doc}
        }
        return self.db_client.update_one(filter_, update)

    async def delete(self, document):
        filter_ = {
            '_id': ObjectId(document.id)
        }
        return self.db_client.delete_one(filter_)
