from typing import Dict, List, Iterable

from node.node_finder import NodeFinder
from operations.mutation.mutation_model_constructor import MutationInputModelConstructor, MutationOutputModelConstructor


# TODO: Please create an Operation CLASS for the __call__() method of Query and Mutation
from operations.mutation.mutation_resolver import MutationResolver


class Mutation:
    """
    TODO: Check if nested NODE documents when deleting a document
        For example we can use a deep_deletion=True parameter that will check all nested documents and delete them
        Obviously don't add deep_deletion=True parameter for subsequent documents
    """

    def __init__(
            self,
            name: str,
            fields: Dict[str, str],
            excluded_input_fields: List[str],
            excluded_output_fields: List[str],
    ):
        self.name = name
        self.create_input_model, self.update_input_model, self.delete_input_model = MutationInputModelConstructor(
            name=name,
            fields=fields,
            excluded_input_fields=excluded_input_fields,
        )
        self.output_model = MutationOutputModelConstructor(
            name=name,
            fields=fields,
            excluded_output_fields=excluded_output_fields
        )

        self.resolver = MutationResolver(
            name=name
        )

    def __call__(self, operation_type: str, input_dict: dict):
        match operation_type:
            case 'create':
                data = await self.resolver.create(
                    self.create_input_model(input_dict)
                )
                return data
            case 'update':
                data = await self.resolver.update(
                    self.update_input_model(input_dict)
                )
                return data
            case 'delete':
                data = await self.resolver.delete(
                    self.delete_input_model(input_dict)
                )
                return 'deleted successfully'
            case 'deep_delete':
                data = await self.resolver.delete(
                    self.delete_input_model(input_dict)
                )
                self._deep_delete(data)
                return 'deleted successfully'

    def _deep_delete(self, data):
        nodes = NodeFinder.get_nodes_list(data)
        for (node_name, object_id) in nodes:
            # Construct a delete input model with object_id and call the dispatcher to delete those nodes
            # We should care about security here! The user's information shall be passed at the same time
            # !! Pass permissions with care !!
            pass

