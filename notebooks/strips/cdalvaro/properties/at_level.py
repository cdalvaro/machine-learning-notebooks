from .base_property import BaseProperty
from ..element import Element
from ..singleton import Singleton


class Level:

    def __init__(self, level: int, name: str):
        """
        Clase base para modelizar un nivel.

        Args:
            level (int): Valor del nivel.
            name (str): Nombre del nivel.
        """
        self.level: int = level
        self.name: str = name

    def __str__(self) -> str:
        return self.name

    def __eq__(self, other) -> bool:
        return self.level == other.level


class TopLevel(Level, metaclass=Singleton):

    def __init__(self):
        """ Clase singleton para representar el nivel superior. """
        super().__init__(1, 'Superior')


class GroundLevel(Level, metaclass=Singleton):

    def __init__(self):
        """ Clase singleton para representar el nivel inferior. """
        super().__init__(0, 'Inferior')


class AtLevel(BaseProperty):

    def __init__(self, element: Element, level: Level, position: int = None):
        """
        Clase para modelizar la propiedad de posición vertical.

        Args:
            element (Element): Objeto que se encuentra en el nivel indicado.
            level (Level): Nivel en el que se encuentra el objeto.
        """
        name = f"{element}EnNivel{level}"
        if level == TopLevel():
            if position is None:
                raise ValueError("Missing position at top level")
            name += f"EnPosicion{position}"
        weight = 0

        super().__init__(name, weight)
        self.element: Element = element
        self.level: Level = level
        self.position: int = position
