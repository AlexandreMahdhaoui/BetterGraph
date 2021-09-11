from typing import Dict, List, Optional, Any, Union

from pydantic import BaseModel

from better_graph.utils.base_model import InputModel, OutputModel
from better_graph.utils.check_type import check_instance
from better_graph.utils.typing_parser import TypingParser as tp
from better_graph.utils.str_converter import StringConverter as sc


#   TODO: MERGE Input and Output Constructor

class QueryInputModel(InputModel):
    name: str
    query_params: Dict[str, Any]
    projection: Dict[str, Union[str, Dict[str, Any]]]


class QueryInputModelConstructor:
    def __new__(
            cls,
            name: str,
            projection: Dict[str, str],
            excluded_input_fields: List[str]
    ) -> type(QueryInputModel):
        check_instance(name, str)
        name = '{}_query_input_model'.format(name)

        projection_ = tp.parse_fields(
            fields=projection, excluded_fields=excluded_input_fields, make_optional=True, is_query_input=True
        )
        ProjectionModel = type('ProjectionModel', (InputModel,), {'__annotations__': projection_})

        model = type(
            sc.snake_to_pascal(name),
            (QueryInputModel,),
            {
                '__annotations__': {
                    'name': str,
                    'query_params': Optional[Dict[str, str]],  # QueryParamsModel,
                    'projection': ProjectionModel
                }
            }
        )
        return model


class QueryOutputModelConstructor:
    def __new__(
            cls,
            name: str,
            fields: Dict[str, str],
            excluded_output_fields: List[str]
    ) -> type(BaseModel):
        if not isinstance(name, str):
            raise (TypeError, "type of 'name' must be: str")
        name = '{}_query_output_model'.format(name)

        fields_ = tp.parse_fields(fields=fields, excluded_fields=excluded_output_fields, make_optional=True)

        model = type(
            sc.snake_to_pascal(name),
            (OutputModel,),
            {
                '__annotations__': fields_,
            }
        )
        return model
