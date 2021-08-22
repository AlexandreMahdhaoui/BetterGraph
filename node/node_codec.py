from typing import Tuple

from utils.check_type import check_instance
from base64 import standard_b64encode, standard_b64decode


class NodeCodec:
    separator: str = ': '

    @classmethod
    def encode(cls, node_name: str, object_id: str):
        check_instance(node_name, str), check_instance(object_id, str)
        s = cls.separator.join([node_name, object_id])
        return '__NODE__{}'.format(cls._b64_encode(s))

    @classmethod
    def decode(cls, encoded_node: str) -> Tuple[str, str]:
        check_instance(encoded_node, str)
        s = encoded_node.replace('__NODE__', '')
        s_ = cls._b64_decode(s)
        node_name, object_id = s_.split(cls.separator)
        return node_name, object_id

    @classmethod
    def _b64_encode(cls, s: str):
        check_instance(s, str)
        s_ = s.encode('ascii')
        return standard_b64encode(s_).decode('ascii')

    @classmethod
    def _b64_decode(cls, s: str):
        check_instance(s, str)
        s_ = s.encode('ascii')
        return standard_b64decode(s_).decode('ascii')
