from better_graph.utils.typing_parser import TypingParser


class MutationInputModelConstructor:
    def __new__(
            cls,
            name: str,
            fields: dict,
            excluded_input_fields: list
    ):
        # Appending ID to the excluded_creation_fields in case someone were trying to inject corrupted ids
        excluded_creation_fields: list = excluded_input_fields.copy()
        excluded_creation_fields.append('id')

        create_input_model = TypingParser.get_class_model(
            name='{}_create_input_model'.format(name),
            fields=fields,
            excluded_fields=excluded_creation_fields,
            is_input=True
        )
        update_input_model = TypingParser.get_class_model(
            name='{}_create_input_model'.format(name),
            fields=fields,
            excluded_fields=excluded_input_fields,
            is_input=True
        )
        delete_input_model = TypingParser.get_class_model(
            name='{}_delete_input_model'.format(name),
            fields={'id': 'str'},
            excluded_fields=[],
            is_input=True
        )
        return create_input_model, update_input_model, delete_input_model


class MutationOutputModelConstructor:
    def __new__(
            cls,
            name,
            fields,
            excluded_output_fields
    ):
        return TypingParser.get_class_model(
            name='{}_mutation_output_model'.format(name),
            fields=fields,
            excluded_fields=excluded_output_fields
        )
