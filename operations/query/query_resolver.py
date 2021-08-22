import os
from typing import Dict, Any, List

from pymongo import MongoClient

from operations.query.query_model_constructor import QueryInputModel
from utils.query_parser import QueryParser


class QueryResolver:
    def __init__(
            self,
            name: str,
            fields: Dict[str, Any],
            cnx_key: str = "CNX_STR",
            db_name: str = "DB_NAME",
            excluded_query_params: List[str] = None
    ):
        self.name = name
        self.valid_projection_fields = self._get_valid_projection_fields(fields)
        if excluded_query_params:
            self.excluded_query_params = QueryParser.validate_excluded_params(excluded_query_params)

        cnx_str = os.getenv(cnx_key)
        db_name = os.getenv(db_name)
        self.db_client: MongoClient = MongoClient(cnx_str)[db_name]['collection_{}'.format(name)]
        del cnx_str, db_name

    def __call__(self, input_data: QueryInputModel):
        query_params = self._parse_and_validate_query_params(input_data.dict_()['query_params'])
        projection = self._validate_projection(input_data.dict_()['projection'], self.valid_projection_fields)
        return self.db_client.find(query_params, projection)

    def _parse_and_validate_query_params(self, query_params):
        query_params_ = QueryParser.parse(query_params)
        query_params_ = {
            k: v for k, v in query_params_.items() if k in self.valid_projection_fields and k not in self.excluded_query_params
        }
        return query_params_

    def _validate_projection(self, projection, valid_fields):
        projection_ = dict()
        for k, v in projection.__dict__.items():
            if isinstance(v, dict) and k in valid_fields:
                projection_[k] = self._validate_projection(v, valid_fields[k])
            if k in valid_fields:
                projection_[k] = 1
        return projection_

    def _get_valid_projection_fields(self, fields: dict):
        valid_fields = dict()
        for k, v in fields.items():
            try:
                if v.__annotations__:
                    valid_fields[k] = self._get_valid_projection_fields(v.__annotations__)
            except:
                valid_fields[k] = 1
        return valid_fields
