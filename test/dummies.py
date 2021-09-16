import os

import dotenv
from pymongo import MongoClient

dotenv.load_dotenv('.env.test.mongo_db')


class DummyBaseAdapter:
    _namespace = {
        'fromage': MongoClient(os.getenv("CNX_STR"))[os.getenv("DB_NAME")]['collection_{}'.format('fromage')]
    }

    def __class_getitem__(cls, item: str) -> MongoClient:
        return cls._namespace[item]

    def __getitem__(self, item) -> MongoClient:
        return self._namespace[item]
