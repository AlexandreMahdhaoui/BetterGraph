from better_graph.utils.better_types.base_model import BaseModel
from better_graph.utils.typing_parser import TypingParser


class ModelFactory(BaseModel):
    def __init__(
            self,
            model_def: dict,
            types_from_str: bool = False,
            excluded_fields: list = None,
            make_optional: bool = False,
            is_query_input: bool = False,
            **kwargs):
        if not excluded_fields:
            excluded_fields = []
        if types_from_str:
            model_def = TypingParser.parse_fields(
                fields=model_def, excluded_fields=excluded_fields, make_optional=make_optional, is_query_input=is_query_input
            )
        super().__init__(model_def, **kwargs)
