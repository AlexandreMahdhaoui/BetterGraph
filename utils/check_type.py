def check_instance(instance_, class_):
    if not isinstance(instance_, class_):
        raise TypeError('{} must be instance of: {}'.format(instance_, class_))


def check_type(element_, type_):
    if not type(element_) == type_:
        raise TypeError('type({}) must be equal to: {}'.format(element_, type_))
