import json

import pytest
from pymongo import MongoClient

from better_graph.operations.mutation.mutation_resolver import MutationResolver
from test.dummies import DummyBaseAdapter


class TestMutationResolver:
    # TODO: Create tests and assertions document in TEST_MUTATION_RESOLVER.JSON
    def test_mutation_resolver(self):
        for t, a in zip(self.test, self.assertion):
            assert (t == a)

    @pytest.fixture()
    def fixture(self):
        self.setup()
        yield
        self.teardown()

    def setup(self):
        with open('test/operations/query/test_query_resolver.json') as file:
            data = json.load(file)
            self.create_document = data['test']['create']
            self.update_document = data['test']['update']
            self.delete_document = data['test']['delete']
            self.assertion = data['assertion']
        self.name = "fromage"
        self.adapter: MongoClient = DummyBaseAdapter()[self.name]

    def teardown(self):
        pass

    def _set_test(self):
        resolver = MutationResolver(self.name, self.adapter)
        self.test = []
        self.test.extend([x for x in await resolver.create(self.create_document)])
        self.test.extend([x for x in await resolver.update(self.update_document)])
        self.test.extend([x for x in await resolver.delete(self.delete_document)])
