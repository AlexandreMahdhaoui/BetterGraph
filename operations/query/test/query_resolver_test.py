import json
import os
import unittest

from pymongo import MongoClient

from operations.query.query_model_constructor import QueryOutputModelConstructor, QueryInputModelConstructor
from operations.query.query_resolver import QueryResolver


class QueryResolverTest(unittest.TestCase):
    def setUp(self) -> None:
        name = 'fromage'
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
            name=name,
            projection=fields,
            excluded_input_fields=['excluded_input']
        )
        self.output_model = QueryOutputModelConstructor(
            name=name,
            fields=fields,
            excluded_output_fields=['excluded_output']
        )

        self.query_resolver = QueryResolver(
            'fromage',
            self.output_model.__annotations__
        )

        self.input_dict: dict = {
            'name': 'fromage',
            'query_params': dict(),
            'fields': {
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

        cnx_str = os.getenv("CNX_STR")
        db_name = os.getenv("DB_NAME")
        self.collection = MongoClient(cnx_str)[db_name]['collection_{}'.format(name)]
        del cnx_str, db_name
        with open('operations/query/test/query_resolver_test.json') as file:
            data = json.load(file)
            self.documents = data['test']
            self.resolved_data = data['assertion']
        self.collection.insert_many(self.documents)

    def test_query_resolver_call(self):
        cursor = self.query_resolver(self.input_data)
        test = [x for x in cursor]
        assertion = self.resolved_data
        self.assertEqual(test, assertion)

    def tearDown(self) -> None:
        self.collection.drop()
    #   python -m unittest operations/query/test/query_resolver_test.py
