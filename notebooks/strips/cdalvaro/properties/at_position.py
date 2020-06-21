from .base_property import BaseProperty
from ..element import Element, Banana, Monkey


class AtPosition(BaseProperty):

    def __init__(self, element: Element, position: int):
        """
        Clase para modelizar la propiedad de posición hotizontal.

        Args:
            element (Element): Elemento que se encuentra en la posición indicada.
            position (int): Entero con la posición en la que se encuentra el elemento.
        """
        name = f"{element}EnPosicion{position}"
        weight = 1 if element == Banana() else 2 if element == Monkey() else 3

        super().__init__(name, weight)
        self.element: Element = element
        self.position: int = position
