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
        self.name = 'fromage'
        self.adapter: MongoClient = DummyBaseAdapter()[self.name]
        fields = {
            'name': 'str',
            'region': 'Union[List[str], str]',
            'nested': {
                'nested_element': 'str',
                'nested_self': 'str',
                'nested_object_list': 'List[str]'
            },
            'other_node': 'str',
            'excluded_projection_case_0': 'str',
            'excluded_projection_case_1': 'str',
            'excluded_output': 'List[str]',
            'excluded_input': 'Dict[str, str]',
        }
        self.input_model = QueryInputModelConstructor(
            name=self.name,
            projection=fields,
            excluded_input_fields=['excluded_input']
        )
        self.output_model = QueryOutputModelConstructor(
            name=self.name,
            fields=fields,
            excluded_output_fields=['excluded_output']
        )
        self.query_resolver = QueryResolver(
            name=self.name,
            base_adapter=DummyBaseAdapter,
            fields=self.output_model.__annotations__,
            excluded_query_params=['gt']
        )
        self._set_input_dict()
        self._set_base()

    def teardown(self) -> None:
        self.adapter.drop()

    def _set_input_dict(self):
        self.input_dict: dict = {
            'name': self.name,
            'query_params': dict(),
            'projection': {
                'name': 1,
                'region': 1,
                'excluded_output': 1,
                'excluded_input': 1,
                'nested': {
                    'nested_element': 1,
                    'nested_self': 1,
                    'nested_parent': 1
                },
                'other_kind': 1,
                # 'excluded_projection': 1,
            }
        }
        self.input_data = self.input_model(**self.input_dict)

    def _set_base(self):
        self.adapter.drop()
        with open('test/operations/query/test_query_resolver.json') as file:
            data = json.load(file)
            self.documents = data['test']
            self.resolved_data = data['assertion']
        self.adapter.insert_many(self.documents)
