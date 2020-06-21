from .singleton import Singleton


class Element:

    def __init__(self, name: str):
        """
        Clase para representar un elemento genérico.

        Args:
            name (str): Nombre del objeto representado.
        """
        self.name: str = name

    def __str__(self) -> str:
        return self.name

    def __eq__(self, other) -> bool:
        return self.name == other.name


class Monkey(Element, metaclass=Singleton):

    def __init__(self):
        """
        Clase singleton mono.
        """
        super().__init__("🐒")


class Banana(Element, metaclass=Singleton):
    """
    Clase singleton plátano.
    """

    def __init__(self):
        super().__init__("🍌")


class Box(Element, metaclass=Singleton):
    """
    Clase singleton caja.
    """

    def __init__(self):
        super().__init__("📦")
