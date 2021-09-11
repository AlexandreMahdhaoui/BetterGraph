from better_graph.operations.operation import Operation


class BetterGraph:
    _base_instance: object
    operations: dict

    def __init__(
            self,
            name,
            namespace
    ):
        self._name = name
        self._namespace = namespace
        self._base_instance = self._namespace['base']['instance']
        self._config = namespace[name]['config']

        self._init_operations()

    def __call__(self, data: dict):
        if data.get('graph'):
            return self.operations[data['graph']['name']](data['graph'])

    def _init_operations(self):
        for ope in self._config['operations']:
            base_adapter = self._base_instance.get_adapter(microservice=self._name, collection=ope['name'])
            self.operations[ope['name']] = Operation(
                name=ope['name'],
                base_adapter=base_adapter,
                fields=ope['fields'],
                excluded_query_input_fields=ope['excluded_query_input_fields'],
                excluded_query_output_fields=ope['excluded_query_output_fields'],
                excluded_query_params=ope['excluded_query_params'],
                excluded_mutation_input_fields=ope['excluded_mutation_input_fields'],
                excluded_mutation_output_fields=ope['excluded_mutation_output_fields'],
            )

# whole_mutation_example = {
#     'data': {
#         'graph': {
#             'name': 'fromage',
#             'mutation': {
#                 'type': 'create',
#                 'data': { THE MUTATION ENQUIRY }
#             }
#         }
#     }
# }
