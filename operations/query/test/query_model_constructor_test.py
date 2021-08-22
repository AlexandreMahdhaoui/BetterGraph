import unittest
import typing

from pydantic import BaseModel

from operations.query.query_model_constructor import QueryInputModelConstructor, QueryOutputModelConstructor, \
    QueryInputModel


class QueryModelConstructorTest(unittest.TestCase):
    def test_input_model(self):
        test = QueryInputModelConstructor(
            name='fromage',
            projection={
                'id': 'str',
                'name': 'str',
                'country': 'Union[List[str], str]',
                'has_holes': 'Optional[bool]',
                'rate': 'float',
                'sub_fromage': 'str'
            },
            excluded_input_fields=['id']
        )

        class FieldsModel(BaseModel):
            name: typing.Optional[typing.Union[str, int]]
            country: typing.Optional[typing.Union[str, int]]
            has_holes: typing.Optional[typing.Union[str, int]]
            rate: typing.Optional[typing.Union[str, int]]
            sub_fromage: typing.Optional[typing.Union[str, int]]

        class InputModel(QueryInputModel):
            name: str
            query_params: typing.Optional[typing.Dict[str, str]]
            projection: FieldsModel

        assertion = InputModel
        self._check_identity(test, assertion)

    def test_output_model(self):
        test = QueryOutputModelConstructor(
            name='Fromage',
            fields={
                'id': 'str',
                'name': 'str',
                'country': 'Union[List[str], str]',
                'has_holes': 'Optional[bool]',
                'rate': 'float',
                'nested': {
                    'nested_name': 'str',
                    'nested_dict': 'Dict[str,str]',
                    'nested_self': 'str',
                    'nested_parent': 'str'
                },
                'sub_fromage': 'str'
            },
            excluded_output_fields=['has_holes']
        )

        NestedModel = type(
            'NestedModel',
            (BaseModel,),
            {
                '__annotations__':
                    {
                        'nested_name': typing.Optional[str],
                        'nested_dict': typing.Optional[typing.Dict[str, str]],
                        'nested_self': typing.Optional[str],
                        'nested_parent': typing.Optional[str]
                    }
            }
        )

        OutputModelTest = type(
            'OutputModel',
            (BaseModel,),
            {
                '__annotations__': {
                    'id': typing.Optional[str],
                    'name': typing.Optional[str],
                    'country': typing.Optional[typing.Union[typing.List[str], str]],
                    'rate': typing.Optional[float],
                    'nested': typing.Optional[NestedModel],
                    'sub_fromage': typing.Optional[str]
                }
            }
        )

        assertion = OutputModelTest
        self._check_identity(test, assertion)

    def _check_identity(self, test, assertion):
        #  debug(test.__annotations__, assertion.__annotations__)
        self.assertEqual(len(test.__annotations__), len(assertion.__annotations__))
        for (kt, vt), (ka, va) in zip(test.__annotations__.items(), assertion.__annotations__.items()):
            try:
                self.assertEqual(kt, ka)
                self._check_identity(vt, va)
            except:
                try:
                    if type(typing.Optional[typing.Any]) == type(vt):
                        if vt.__dict__['__args__'][0].__annotations__:
                            #  debug(vt.__dict__['__args__'][0].__annotations__)
                            #  debug(va.__dict__['__args__'][0].__annotations__)
                            self._check_identity(vt.__dict__['__args__'][0], va.__dict__['__args__'][0])
                    else:
                        self.assertEqual(vt, va)
                        self.assertEqual(kt, ka)
                except:
                    try:
                        if type(vt) == type(typing.Optional[typing.Any]):
                            for i in range(len(vt.__dict__['__args__'])):
                                self.assertEqual(vt.__dict__['__args__'][i], va.__dict__['__args__'][i])
                        else:
                            self.assertEqual(vt, va)
                            self.assertEqual(kt, ka)
                    except:
                        self.assertEqual(vt, va)
                        self.assertEqual(kt, ka)


if __name__ == '__main__':
    # cd C:\Users\User\Desktop\thinkbetter\CRM\phase_0_3\rest_api
    # python -m unittest operations/query/constructor/test/query_model_constructor_test.py
    unittest.main()
