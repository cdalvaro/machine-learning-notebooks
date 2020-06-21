from .properties import Properties


class State:

    def __init__(self, properties: Properties = None):
        """
        Clase para definir un estado.

        Args:
            properties (Properties, optional): Propiedades que definen el estado. Default: None.
        """
        if properties is None:
            properties = set()
        self.properties: Properties = properties

    def __str__(self) -> str:
        return str(self.properties)
