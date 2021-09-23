import json
import typing

import pytest
from pydantic import BaseModel

from better_graph.operations.mutation.mutation_model_constructor import MutationInputModelConstructor, \
    MutationOutputModelConstructor


class TestMutationModelConstructor:
    def test_mutation_model_constructors(self):
        [self._check_identity(t, a) for t, a in zip(self.test, self.assertion)]

    @pytest.fixture()
    def fixture(self):
        self.setup()
        yield
        self.teardown()

    def setup(self):
        self.test = [
            self.create_input_test,
            self.update_input_test,
            self.delete_input_test,
            self.output_test
        ]
        self.assertion = [
            self.create_input_assertion,
            self.update_input_assertion,
            self.delete_input_assertion,
            self.output_assertion
        ]

    def teardown(self):
        pass

    def _set_test(self):
        with open('test/operations/mutation/test_mutation_model_constructor.json') as file:
            data = json.load(file)
        self.create_input_test, self.update_input_test, self.delete_input_test = MutationInputModelConstructor(
            name=data['test']['name'],
            fields=data['test']['fields'],
            excluded_input_fields=data['test']['excluded_input_fields']
        )
        self.output_test = MutationOutputModelConstructor(
            name=data['test']['name'],
            fields=data['test']['fields'],
            excluded_output_fields=data['test']['excluded_output_fields']
        )

    def _set_assertion(self):
        class NestedModel(BaseModel):
            nested_name: str
            nested_dict: typing.Dict[str, str]
            nested_self: str
            nested_parent: typing.List[str]

        class FromageCreateInputModel(BaseModel):
            name: str
            country: typing.Union[typing.List[str], str]
            nested: NestedModel

        class FromageUpdateInputModel(BaseModel):
            name: str
            country: typing.Union[typing.List[str], str]
            nested: NestedModel

        class FromageDeleteInputModel(BaseModel):
            name: str
            country: typing.Union[typing.List[str], str]
            nested: NestedModel

        class FromageOutputModel(BaseModel):
            id: str
            name: str
            timestamp: str
            nested: NestedModel

        self.create_input_assertion = FromageCreateInputModel
        self.update_input_assertion = FromageUpdateInputModel
        self.delete_input_assertion = FromageDeleteInputModel
        self.output_assertion = FromageOutputModel

    def _check_identity(self, test, assertion):
        assert (len(test.__annotations__) == len(assertion.__annotations__))
        for (kt, vt), (ka, va) in zip(test.__annotations__.items(), assertion.__annotations__.items()):
            try:
                assert (kt == ka)
                self._check_identity(vt, va)
            except:
                self._check_nested_identity(vt, va, kt, ka)

    def _check_nested_identity(self, vt, va, kt, ka):
        try:
            if type(typing.Optional[typing.Any]) == type(vt):
                if vt.__dict__['__args__'][0].__annotations__:
                    #  debug(vt.__dict__['__args__'][0].__annotations__)
                    #  debug(va.__dict__['__args__'][0].__annotations__)
                    self._check_identity(vt.__dict__['__args__'][0], va.__dict__['__args__'][0])
            else:
                assert (vt == va)
                assert (kt == ka)
        except:
            self._check_even_more_nested_identity(vt, va, kt, ka)

    def _check_even_more_nested_identity(self, vt, va, kt, ka):
        try:
            if type(vt) == type(typing.Optional[typing.Any]):
                for i in range(len(vt.__dict__['__args__'])):
                    assert (vt.__dict__['__args__'][i] == va.__dict__['__args__'][i])
            else:
                assert (vt == va)
                assert (kt == ka)
        except:
            assert (vt == va)
            assert (kt == ka)