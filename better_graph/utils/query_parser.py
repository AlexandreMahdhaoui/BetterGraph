import typing

comparison = ('eq', 'gt', 'in', 'lt', 'lte', 'ne', 'nin')
logical = ('and', 'not', 'nor', 'or')
element = ('exists', 'type')
evaluation = ('expr', 'jsonSchema', 'mod', 'regex', 'text', 'where')
geospatial = ('geoIntersects', 'geoWithin', 'near', 'nearSphere')
array = ('all', 'elemMatch', 'size')


class QueryParser:
    """
    TODO:
        Implement method: validate EXCLUDED_PARAMS: List[str]
        Implement: AND, NOT, NOR & OR params
            ----> Support the case where "key.split('__').__len__() > 2"
        Implement: REGEX
    """
    valid_params = ('eq', 'gt', 'in', 'lt', 'lte', 'ne', 'nin')

    @classmethod
    def parse(cls, query_params: typing.Dict[str, str], excluded_params: typing.List[str] = None):
        d_ = dict()
        for key, value in query_params.items():
            field, param = key.split('__')
            if excluded_params:
                if param in cls.valid_params and param not in excluded_params:
                    cls._populate_dict(param, field, d_, value)
            if not excluded_params and param in cls.valid_params:
                cls._populate_dict(param, field, d_, value)
        return d_

    @classmethod
    def _populate_dict(cls, param, field, d_, value):
        param = '${}'.format(param)
        if field not in d_:
            d_[field] = dict()
        d_[field][param] = value

    @classmethod
    def validate_excluded_params(cls, excluded_params: typing.List[str]):
        return [p for p in excluded_params if excluded_params in cls.valid_params]
