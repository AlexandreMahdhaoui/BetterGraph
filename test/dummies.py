import os

import dotenv
from pymongo import MongoClient

dotenv.load_dotenv('.env.test.mongo_db')
cnx_str = os.getenv("CNX_STR")
db_name = os.getenv("DB_NAME")


class DummyBaseAdapter:
    _namespace = {
        'fromage': MongoClient(cnx_str)[db_name]['collection_{}'.format('fromage')]
    }

    def __class_getitem__(cls, item: str) -> MongoClient:
        return cls._namespace[item]

    def __getitem__(self, item) -> MongoClient:
        return self._namespace[item]
