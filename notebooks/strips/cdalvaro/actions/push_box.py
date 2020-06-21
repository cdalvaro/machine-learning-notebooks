from .base_action import BaseAction
from ..element import Box, Monkey
from ..properties import AtLevel, GroundLevel, AtPosition


class PushBox(BaseAction):

    def __init__(self, from_position: int, to_position: int):
        """
        Clase con la acción de empujar la caja.

        Esta clase modeliza la operación de empujar la caja de una posición a otra.

        Args:
            from_position (int): Posición desde la que se va a mover el elemento.
            to_position (int): Posición a la que se va a mover el elemento.
        """
        name = f"{Monkey()} empuja la {Box()} de {from_position} a {to_position}"
        weight = 1

        super().__init__(name, weight)
        self.from_position: int = from_position
        self.to_position: int = to_position

        self._set_precondition()
        self._set_add_list()
        self._set_remove_list()

    def _set_precondition(self):
        """
        * La caja se encuentra en la posición de partida
        * El mono se encuentra en la posición de partida
        * El mono está en el nivel inferior
        """
        self.precondition.add(AtPosition(Box(), self.from_position))
        self.precondition.add(AtPosition(Monkey(), self.from_position))
        self.precondition.add(AtLevel(Monkey(), GroundLevel(), self.from_position))

    def _set_add_list(self):
        """
        * La caja estará en la nueva posición
        * El mono estará en la nueva posición
        """
        self.add_list.add(AtPosition(Box(), self.to_position))
        self.add_list.add(AtPosition(Monkey(), self.to_position))

    def _set_remove_list(self):
        """
        * La caja dejará de estar en la posición de origen
        * El mono dejará de estar en la posición de origen
        """
        self.remove_list.add(AtPosition(Box(), self.from_position))
        self.remove_list.add(AtPosition(Monkey(), self.from_position))
