import unittest
import typing

from devtools import debug
from pydantic import BaseModel

from utils.typing_parser import TypingParser as tp
from utils.str_converter import StringConverter as sc


class TypingParserTest(unittest.TestCase):
    def test_str_to_type(self):
        test = ['Optional', 'List', 'list', 'str', 'None', 'NoneType']
        assertion = [typing.Optional, typing.List, 'list', 'str', None, None]
        intended_error = 'fromage'

        for t, a in zip(test, assertion):
            t_ = tp._str_to_type(t)
            self.assertEqual(t_, a)
        with self.assertRaises(TypeError):
            tp._str_to_type(intended_error)

    def test_make_str_optional(self):
        test = ['typing.Dict', 'list', 'str']
        assertion = ['typing.Optional[typing.Dict]', 'typing.Optional[list]', 'typing.Optional[str]']
        intended_error = int
        for t, a in zip(test, assertion):
            t_ = tp._make_str_optional(t)
            self.assertEqual(t_, a)
        with self.assertRaises(TypeError):
            tp._str_to_type(intended_error)

    def test_parse_nested_dict(self):
        test = {
            'fromage': 'Optional[Dict]',
            'camembert': 'List[Union[str, Dict[str, int], int]]',
            'even_more_nested': {
                'very_nested_dict': 'Dict',
                'cheese is great': 'bool',
                'parent': 'str'
            }
        }
        EvenMoreNested = type(
            sc.snake_to_pascal('even_more_nested'),
            (BaseModel,),
            {
                '__annotations__': {
                    'very_nested_dict': typing.Dict,
                    'cheese is great': bool,
                    'parent': str
                }
            }
        )

        class Assertion(BaseModel):
            fromage: typing.Optional[typing.Dict]
            camembert: typing.List[typing.Union[str, typing.Dict[str, int], int]]
            even_more_nested: EvenMoreNested
            parent_test: str

        t_ = tp._parse_nested_dict(test, key='test')

        for t, a in zip(t_.__annotations__, Assertion.__annotations__):
            self.assertEqual(t, a)
        self.assertEqual(
            t_.__annotations__['even_more_nested'].__annotations__,
            Assertion.__annotations__['even_more_nested'].__annotations__
        )

    def test_parse(self):
        test = 'List[Union[str, Dict[str, int], int]]'
        t_ = [
            tp.parse(test, make_optional=False),
            tp.parse(test, make_optional=True),
            tp.parse(test, is_query_input=True),
        ]
        assertion = [
            typing.List[typing.Union[str, typing.Dict[str, int], int]],
            typing.Optional[typing.List[typing.Union[str, typing.Dict[str, int], int]]],
            typing.Optional[typing.Union[str, int]],
        ]
        intended_error = 'List[Union[str, Dict,int]'
        for t, a in zip(t_, assertion):
            self.assertEqual(t, a)
        with self.assertRaises(SyntaxError):
            tp.parse(intended_error)


if __name__ == '__main__':
    # python -m unittest utils/test/typing_parser_test.py
    unittest.main()
