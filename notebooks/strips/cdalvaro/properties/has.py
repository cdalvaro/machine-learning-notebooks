from .base_property import BaseProperty
from ..element import Element


class Has(BaseProperty):

    def __init__(self, owner: Element, element: Element):
        """
        Clase para modelizar la propiedad de tener plátano.

        Args:
            owner (Element): Elemento que posee al otro elemento.
            element (Element): Elemento posesión del owner.
        """
        name = f"{owner}Tiene{element}"
        weight = 0

        super().__init__(name, weight)
        self.owner: Element = owner
        self.element: Element = element
