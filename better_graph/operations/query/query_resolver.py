from typing import Dict, Any, List
from better_graph.operations.query.query_model_constructor import QueryInputModel
from better_graph.utils.query_parser import QueryParser


class QueryResolver:
    """
        TODO: Refactor db_client to call a BetterBase? or BetterAdapter? class
            > We don't want to create the db_client instance here but rather ask for a distant library to create
              it from a default_config file
    """
    def __init__(
            self,
            name: str,
            base_adapter,
            fields: Dict[str, Any],
            excluded_query_params: List[str] = None
    ):
        self.name = name
        self.valid_projection_fields = self._get_valid_projection_fields(fields)
        if excluded_query_params:
            self.excluded_query_params = QueryParser.validate_excluded_params(excluded_query_params)

        self.base_adapter = base_adapter[name.lower()]

    def __call__(self, input_data: QueryInputModel):
        query_params = self._parse_and_validate_query_params(input_data.dict_()['query_params'])
        projection = self._validate_projection(input_data.dict_()['projection'], self.valid_projection_fields)
        return self.base_adapter.find(query_params, projection)

    def _parse_and_validate_query_params(self, query_params):
        query_params_ = QueryParser.parse(query_params, excluded_params=self.excluded_query_params)
        query_params_ = {
            k: v for k, v in query_params_.items() if
            k in self.valid_projection_fields and k not in self.excluded_query_params
        }
        return query_params_

    def _validate_projection(self, projection, valid_fields):
        projection_ = dict()
        for k, v in projection.items():
            if isinstance(v, dict) and k in valid_fields:
                projection_[k] = self._validate_projection(v, valid_fields[k])
            elif k in valid_fields and str(v) == '1':
                projection_[k] = 1
        return projection_

    def _get_valid_projection_fields(self, fields: dict):
        # atm: We only check for one level of nesting
        # TODO: allow recursion of values of nested dictionaries or lists
        #   > means: implementing the logic to read such nested components
        valid_fields = dict()
        for k, v in fields.items():
            if hasattr(v, '__dict__') and '__args__' in v.__dict__:
                nested = [x for x in map(self._get_valid_projection_fields,
                                         [x.__annotations__ for x in v.__dict__['__args__']
                                          if isinstance(x, type) and hasattr(x, '__annotations__')]) if x]
                # if instance type it's a class and if hasattr(annotations) it's a BaseModel (not 100% true)
                if nested:
                    if nested.__len__() == 1:
                        valid_fields[k] = nested.__getitem__(0)
                        continue
                    else:
                        valid_fields[k] = nested
                        continue
            if hasattr(v, '__annotations__'):
                valid_fields[k] = self._get_valid_projection_fields(v.__annotations__)
                continue
            valid_fields[k] = 1
            continue
        return valid_fields
