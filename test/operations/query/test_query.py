import json

import pytest
from devtools import debug
from pymongo import MongoClient

from better_graph.operations.query.query import Query
from test.dummies import DummyBaseAdapter


#  TODO: !!RESOLVED!!
#   Please find a solution to Pydantic's _id problem
#       Either don't use Pydantic at all
#       Or build a resolver method converting _id to id
#           For this solution we should implement the use of ObjectID:
#               bson.objectid.ObjectId(_id).__str__() to get _id as a string

class QueryTest:

    def test_query(self):
        test = [t.dict() for t in self.query(self.test)]
        assertion = [self.assertion]
        debug(test, assertion)
        assert (test == assertion)

    @pytest.fixture
    def fixture(self):
        self.setup()
        yield
        self.teardown()

    def setup(self) -> None:
        with open('better_graph/operations/query/test/test_query.json') as file:
            data = json.load(file)
            name: str = data['query_model']['name']
            self.query = Query(
                name=name,
                fields=data['query_model']['fields'],
                base_adapter=DummyBaseAdapter,
                excluded_query_params=data['query_model']['excluded_query_params'],
                excluded_input_fields=data['query_model']['excluded_input_fields'],
                excluded_output_fields=data['query_model']['excluded_output_fields']
            )
            self.test = data['test']
            self.assertion = data['assertion']
            self.documents = data['documents']

            self.adapter: MongoClient = DummyBaseAdapter()[name]
            self.adapter.insert_many(self.documents)

    def teardown(self) -> None:
        self.adapter.drop()
