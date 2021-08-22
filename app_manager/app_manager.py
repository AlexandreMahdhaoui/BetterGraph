class AppManager:
    """
    AppManager's roles:
        Provide an interface between the client and it's application
        Provides an administration REST API at '/api-admin'

        Loads RESOURCES and expose them to the '/api' route

    params:
        config
        mode: str
            - 'from_db': Reads a config file from a Mongo Database
                This config file must specify to the: GraphBetter Configuration Specification
                    Indeed this config file can be administrated in live.
                    AppManager gives an endpoint '/api-admin' (instead of '/api') that helps manage the app's configuration
            - 'json': Reads a config file written in json
    """
    def __init__(
            self,
            **kwargs
    ):
        pass
