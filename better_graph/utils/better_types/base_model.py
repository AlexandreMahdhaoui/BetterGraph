from abc import ABC
from json import dumps as json_dumps
from better_graph.utils.better_types.type_check import TypeCheck


class BaseModel(ABC):
    def __init__(
            self,
            model_def,
            name='base_model',
            **kwargs):
        self._name = name
        self._model_def = model_def
        self.__annotations__ = {k: v for k, v in model_def.items() if isinstance(k, str)}

    def __call__(self, data, __json__: bool = False):
        return self._serialize(data) if not __json__ else json_dumps(self._serialize(data))

    def _serialize(self, data):
        keys = data.keys()
        return {k: data[k] for k, v in self._types if k in keys and TypeCheck(value=data[k], type_=v, name=k, model_name=self._name)}

    @property
    def _types(self):
        return self.__annotations__.items()
