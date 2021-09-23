import typing

_SpecialForm = typing._SpecialForm


class TypeCheck:
    """
    does not check nested levels
    """

    def __new__(cls, value, type_, name, model_name):
        return cls._check_type(value, type_, name, model_name)

    @classmethod
    def _find_type_origin(cls, t):
        if isinstance(t, _SpecialForm):
            return
        actual_type = typing.get_origin(t) or t
        if isinstance(actual_type, _SpecialForm):
            for origins in map(cls._find_type_origin, typing.get_args(t)):
                yield from origins
        else:
            yield actual_type

    @classmethod
    def _check_type(cls, value, type_, name, model_name):
        actual_types = tuple(cls._find_type_origin(type_))
        if actual_types and not isinstance(value, actual_types):
            raise TypeError("Expected type '{}' for argument '{}' of model '{}' but received type '{}' instead."
                            .format(type_, name, model_name, type(value)))
        return True

