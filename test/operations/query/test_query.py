import json

import pytest
from bson import ObjectId
from devtools import debug
from pymongo import MongoClient

from better_graph.operations.query.query import Query
from test.dummies import DummyBaseAdapter


class TestQuery:
    """
    TODO: PLEASE REFACTOR PROJECTION VALIDATION
    TODO: CREATE A PROJECTION PARSING AND VALIDATING CLASS
    """
    def test_query(self):
        test = [t for t in self.query(self.test)]
        assertion = [self.assertion]
        assert test == assertion

    @pytest.fixture
    def fixture(self):
        self.setup()
        yield
        self.teardown()

    def setup(self) -> None:
        with open('test/operations/query/test_query.json') as file:
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
        self.assertion['id'] = ObjectId(self.assertion['id'])
        self.documents = data['documents']

        self.adapter: MongoClient = DummyBaseAdapter()[name]
        self.adapter.insert_many(self.documents)

    def teardown(self) -> None:
        self.adapter.drop()
