from better_graph.operations.mutation.mutation import Mutation
from better_graph.operations.query.query import Query


class Operation:
    def __init__(
            self,
            name,
            base_adapter,
            fields,
            excluded_query_input_fields,
            excluded_query_output_fields,
            excluded_query_params,
            excluded_mutation_input_fields,
            excluded_mutation_output_fields,
    ):
        self.query = Query(
            name=name,
            fields=fields,
            base_adapter=base_adapter,
            excluded_input_fields=excluded_query_input_fields,
            excluded_output_fields=excluded_query_output_fields,
            excluded_query_params=excluded_query_params,
        )
        self.mutation = Mutation(
            name=name,
            base_adapter=base_adapter,
            fields=fields,
            excluded_input_fields=excluded_mutation_input_fields,
            excluded_output_fields=excluded_mutation_output_fields,
        )

    def __call__(self, graph):
        if graph.get('query'):
            return self.query(graph['query'])
        if graph.get('mutation'):
            return self.mutation(
                operation_type=graph['mutation']['type'],
                input_dict=graph['mutation']['data']
            )


# whole_mutation_example = {
#     'data': {
#         'graph': {
#             'name': 'fromage',
#             'mutation': {
#                 'type': 'create',
#                 'data': { THE MUTATION QUERY }
#             }
#         }
#     }
# }
