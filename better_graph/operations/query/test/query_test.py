import json
import os

import pytest
from devtools import debug
from pymongo import MongoClient

from better_graph.operations.query.query import Query


#  TODO: DONE
#   Please find a solution to Pydantic's _id problem
#       Either don't use Pydantic at all
#       Or build at resolver method a _id to id converter
#           For this solution we should implement the use of ObjectID:
#               bson.objectid.ObjectId(_id).__str__() to get _id as a string


class QueryTest:
    @pytest.fixture
    def fixture(self):
        self.setup()
        yield
        self.teardown()

    def test_query(self):
        test = [t.dict() for t in self.query(self.test)]
        assertion = [self.assertion]
        debug(test, assertion)
        assert(test == assertion)

    def setup(self) -> None:
        with open('better_graph/operations/query/test/query_test.json') as file:
            data = json.load(file)
            self.query = Query(
                name=data['query_model']['name'],
                fields=data['query_model']['fields'],
                excluded_query_params=data['query_model']['excluded_query_params'],
                excluded_input_fields=data['query_model']['excluded_input_fields'],
                excluded_output_fields=data['query_model']['excluded_output_fields']
            )
            self.test = data['test']
            self.assertion = data['assertion']
            self.documents = data['documents']

            cnx_str = os.getenv("CNX_STR")
            db_name = os.getenv("DB_NAME")
            self.collection = MongoClient(cnx_str)[db_name]['collection_{}'.format('fromage')]
            self.collection.insert_many(self.documents)

    def teardown(self) -> None:
        self.collection.drop()
