from .base_action import BaseAction
from ..element import Element, Monkey
from ..properties import AtLevel, GroundLevel, AtPosition


class MoveHorizontally(BaseAction):

    def __init__(self, element: Element, from_position: int, to_position: int):
        """
        Clase con la acción de movimiento horizontal.

        Esta clase modeliza el movimiento de un elemento en el plano horizontal.

        Args:
            element (Element): Elemento que se va a mover.
            from_position (int): Posición desde la que se va a mover el elemento.
            to_position (int): Posición a la que se va a mover el elemento.
        """
        name = f"Mueve {element} de {from_position} a {to_position}"
        weight = 2

        super().__init__(name, weight)
        self.element: Element = element
        self.from_position: int = from_position
        self.to_position: int = to_position

        self._set_precondition()
        self._set_add_list()
        self._set_remove_list()

    def _set_precondition(self):
        """
        * El elemento se encuentra en la posición: 'from_position'
        * Si el elemento es el mono, el mono se encuentra en el nivel inferior
        """
        self.precondition.add(AtPosition(self.element, self.from_position))
        if type(self.element) == Monkey:
            self.precondition.add(AtLevel(Monkey(), GroundLevel(), self.from_position))

    def _set_add_list(self):
        """
        * El elemento se encontrará en la posición: 'to_position'
        """
        self.add_list.add(AtPosition(self.element, self.to_position))

    def _set_remove_list(self):
        """
        * El elemento dejará de estar en la posición: 'from_position'
        """
        self.remove_list.add(AtPosition(self.element, self.from_position))
