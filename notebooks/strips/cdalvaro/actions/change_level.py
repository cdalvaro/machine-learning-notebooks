from .base_action import BaseAction
from ..element import Box, Monkey
from ..properties import Level, TopLevel, GroundLevel, AtPosition, AtLevel


class ChangeLevel(BaseAction):

    def __init__(self, position: int, to_level: Level):
        """
        Clase con la acción de cambiar de nivel.

        Esta clase modeliza el movimiento del mono para cambiar de nivel.

        Args:
            position (int): Posición horizontal en la que se encuentra el mono.
            to_level (Level): Nivel en el que finalizará el mono.
        """
        name = f"Cambia {Monkey()} al nivel {to_level} en posición {position}"
        weight = 3

        super().__init__(name, weight)
        self.position: int = position
        self.to_level: Level = to_level
        self.from_level: Level = GroundLevel() if to_level == TopLevel() else TopLevel()

        self._set_precondition()
        self._set_add_list()
        self._set_remove_list()

    def _set_precondition(self):
        """
        * La caja se encuentra en la posición 'position'
        * El mono se encuentra en la posición 'position'
        * El mono está en el nivel opuesto al que se va a mover
        """
        self.precondition.add(AtPosition(Box(), self.position))
        self.precondition.add(AtPosition(Monkey(), self.position))
        self.precondition.add(AtLevel(Monkey(), self.from_level, self.position))

    def _set_add_list(self):
        """
        * El mono estará en el nivel objetivo
        """
        self.add_list.add(AtLevel(Monkey(), self.to_level, self.position))

    def _set_remove_list(self):
        """
        * El mono dejará de estar en el nivel de origen
        """
        self.remove_list.add(AtLevel(Monkey(), self.from_level, self.position))
