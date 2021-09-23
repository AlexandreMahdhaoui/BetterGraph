import json
import pytest
from pymongo import MongoClient

from better_graph.operations.query.query_model_constructor import QueryOutputModelConstructor, \
    QueryInputModelConstructor
from better_graph.operations.query.query_resolver import QueryResolver
from test.dummies import DummyBaseAdapter


class TestQueryResolver:

    def test_query_resolver_call(self, fixture):
        cursor = self.query_resolver(self.input_data)
        test = [x for x in cursor]
        assertion = self.resolved_data
        assert (test == assertion)

    @pytest.fixture()
    def fixture(self):
        self.setup()
        yield
        self.teardown()

    def setup(self) -> None:
        with open('test/operations/query/test_query_resolver.json') as file:
            data = json.load(file)
            self.fields = data['fields']
            self.input_dict = data['input_dict']
            self.documents = data['test']
            self.resolved_data = data['assertion']
        self.name = 'fromage'
        self.adapter: MongoClient = DummyBaseAdapter()[self.name]
        self.input_model = QueryInputModelConstructor(
            name=self.name,
            projection=self.fields,
            excluded_input_fields=['excluded_input']
        )
        self.output_model = QueryOutputModelConstructor(
            name=self.name,
            fields=self.fields,
            excluded_output_fields=['excluded_output']
        )
        self.query_resolver = QueryResolver(
            name=self.name,
            base_adapter=DummyBaseAdapter,
            fields=self.output_model.__annotations__,
            excluded_query_params=['gt']
        )
        self._set_input_data()
        self._set_base()

    def teardown(self) -> None:
        self.adapter.drop()

    def _set_input_data(self):
        self.input_data = self.input_model(**self.input_dict)

    def _set_base(self):
        self.adapter.drop()
        self.adapter.insert_many(self.documents)
