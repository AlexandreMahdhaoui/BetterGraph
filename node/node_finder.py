from node.node_codec import NodeCodec


class NodeFinder:
    """
    TODO: We are not recursively checking List of items
            For example if we have a list of dictionaries we should be able to recursively checking if
            the dictionaries in the list contains nodes
            How to build path if we have a dictionaries then list of dict
    method find_node:
        Looks for : '__NODE__{node_codec.encode("{name}: {object_id}")}' VALUE in OutputModels
        --> Returns a dictionary with:
            KEY: original_dictionary's path
            VALUE: (node_name, object_id) tuples as VALUE
    """
    PATH_MERGER: str = '.{}'
    PATH_SEPARATOR: str = '.'
    NODE_TRIGGER: str = '__NODE__'

    @classmethod
    def find_nodes(cls, d: dict, path: str = '', node_dict: dict = None):
        """
        NodeFinder.find_nodes() is a method that finds a node with it's path and returns a dictionnary
            {'path': (node_name, object_id)} Dict[str, Tuple(str, str)]
        """
        if not node_dict:
            node_dict = dict()
        for k, v in d.items():
            path_ = cls._merge_path(path, k)
            if isinstance(v, str):
                if v.startswith(cls.NODE_TRIGGER):
                    cls._populate_node_dict(v, node_dict, path_)
            if isinstance(v, dict):
                node_dict = cls.find_nodes(v, path=path_, node_dict=node_dict)
            if isinstance(v, list):
                node_list = cls._get_nodes_from_list(v)
                if node_list:
                    node_dict[path] = node_list
        return node_dict

    @classmethod
    def get_nodes_list(cls, d: dict, _list=None):
        """
        Recursively find nodes in a dict and returns a list of tuple (node_name, object_id)
        """
        if not _list:
            _list = []
        for v in d.values():
            if isinstance(v, str):
                if v.startswith(cls.NODE_TRIGGER):
                    node_name, object_id = NodeCodec.decode(v)
                    _list.append((node_name, object_id))
            if isinstance(v, dict):
                _list.extend(cls.get_nodes_list(v, _list=_list))
        return _list

    @classmethod
    def inject_nodes(cls, original_dict: dict, injection_dict: dict):
        dict_ = original_dict.copy()
        for path, resolution in injection_dict.items():
            dict_ = cls.resolve_node(dict_, path, resolution)
        return dict_

    @classmethod
    def _populate_node_dict(cls, value, node_dict, path):
        node_name, object_id = NodeCodec.decode(value)
        node_dict[path] = (node_name, object_id)

    @classmethod
    def _get_nodes_from_list(cls, value):
        l_ = []
        checker = 1
        for item in value:
            checker *= 0
            if isinstance(item, str):
                if item.startswith(cls.NODE_TRIGGER):
                    checker = 1
                    node_name, object_id = NodeCodec.decode(item)
                    l_.append((node_name, object_id))
        if not checker:
            return None
        return l_

    @classmethod
    def _parse_path(cls, path: str) -> list:
        return [k for k in path.split(cls.PATH_SEPARATOR) if k]

    @classmethod
    def _merge_path(cls, current_path, current_key):
        if not current_path == '':
            return cls.PATH_MERGER.join((current_path, '')).format(current_key)
        return current_key

    @classmethod
    def resolve_node(cls, d: dict, path: str, resolution):
        dict_ = d.copy()
        keys: list = cls._parse_path(path)
        x = dict_
        if not keys.__len__() == 1:
            for key in keys[:-1]:
                x = x[key]
        x[keys[-1]] = resolution
        return dict_
