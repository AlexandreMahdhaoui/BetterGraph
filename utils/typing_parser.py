import typing
import re

from pydantic import BaseModel

from utils.base_model import InputModel, OutputModel
from utils.check_type import check_instance
from utils.str_converter import StringConverter as sc, StringConverter


class TypingParser:
    """
    TODO: // NOT FOR NOW // Implementation of __NODE__type // NOT FOR NOW //
    """
    custom_types: typing.Dict = dict()

    @classmethod
    def parse(
            cls,
            value: typing.Union[str, dict],
            key: str = None,
            make_optional: bool = False,
            is_query_input: bool = None
    ) -> typing.Union[typing.Type, str]:

        if isinstance(value, dict):
            if make_optional:
                return typing.Optional[cls._parse_nested_dict(
                    value, key=key, make_optional=make_optional, is_query_input=is_query_input
                )]
            return cls._parse_nested_dict(value, key)

        check_instance(value, str)

        if is_query_input:
            return typing.Optional[typing.Union[str | int]]

        if make_optional:
            if not isinstance(make_optional, bool):
                raise TypeError('make_optional must be type: bool')
            return eval(cls._make_str_optional(cls._parse_str(value)))
        return eval(cls._parse_str(value))

    @classmethod
    def parse_fields(
            cls,
            fields: typing.Dict,
            excluded_fields: typing.List[str],
            make_optional: bool = False,
            is_query_input: bool = False
    ):
        return {
            k: TypingParser.parse(v, key=k, make_optional=make_optional, is_query_input=is_query_input) \
            for k, v in fields.items() \
            if k not in excluded_fields
        }

    # TODO: implement get_class_model returning a model
    @classmethod
    def get_class_model(
            cls,
            name: str,
            fields: dict,
            excluded_fields: list,
            make_optional: bool = False,
            is_input: bool = False,
            is_query: bool = False
    ):
        is_query_input = (is_query and is_input)
        fields_ = cls.parse_fields(
            fields=fields,
            excluded_fields=excluded_fields,
            make_optional=make_optional,
            is_query_input=is_query_input
        )
        return type(
            StringConverter.snake_to_pascal(name),
            (OutputModel if not is_input else InputModel,),
            {
                '__annotations__': fields_
            }
        )

    @classmethod
    def _parse_nested_dict(
            cls,
            dict_: dict,
            key: str,
            make_optional: bool = False,
            is_query_input: str = None
    ):
        nested_name = '{}Model'.format(sc.snake_to_pascal(key))
        nested_fields = {
            k: cls.parse(v, key=k, make_optional=make_optional, is_query_input=is_query_input) for k, v in dict_.items()
        }
        return type(
            nested_name,
            (BaseModel,),
            {'__annotations__': nested_fields}
        )

    @classmethod
    def _make_str_optional(cls, str_: str) -> str:
        if not isinstance(str_, str):
            raise TypeError('Please provide an argument of type: str')
        return 'typing.Optional[{}]'.format(str_)

    @classmethod
    def _parse_str(cls, str_: str):
        list_ = re.sub("[0-9a-zA-Z]", " ", str_).split(' ')  # Remove all alphanumerical
        pre_format = '{}' + '{}'.join([s for s in list_ if s])
        list__ = re.sub("[^0-9a-zA-Z]+", '_', str_).split('_')  # Remove non-alphanumerical
        sanitized_ = [cls._str_to_type(s) for s in list__ if s]
        return pre_format.format(*sanitized_)

    @classmethod
    def _str_to_type(cls, str_: str):
        builtins = {
            'int': int,
            'float': float,
            'str': str,
            'list': list,
            'dict': dict,
            'bool': bool
        }
        if str_ == 'None' or str_ == 'NoneType':
            return None
        if str_ in builtins:
            return str_
        else:
            if str_ in typing.__dict__:
                return typing.__dict__[str_]
            else:
                raise TypeError('invalid type of element: {}'.format(str(str_)))

