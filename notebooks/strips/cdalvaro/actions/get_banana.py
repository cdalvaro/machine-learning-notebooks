from .base_action import BaseAction
from ..element import Banana, Box, Monkey
from ..properties import AtLevel, TopLevel, AtPosition, Has


class GetBanana(BaseAction):

    def __init__(self, position: int):
        """
        Clase con la acción de conseguir un plátano.

        Esta clase modeliza la acción de que el mono consiga el plátano.

        Args:
            position (int): Posición en la que el mono consigue el plátano.
        """
        name = f"{Monkey()} consigue {Banana()} en posición {position}"
        weight = 4

        super().__init__(name, weight)
        self.position: int = position

        self._set_precondition()
        self._set_add_list()
        self._set_remove_list()

    def _set_precondition(self):
        """
        * La caja se encuentra en la posición: 'position'
        * El mono se encuentra en la posición: 'position'
        * El mono se encuentra en el nivel superior
        * El plátano se encuentra en la posición: 'position'
        """
        self.precondition.add(AtPosition(Box(), self.position))
        self.precondition.add(AtPosition(Monkey(), self.position))
        self.precondition.add(AtPosition(Banana(), self.position))
        self.precondition.add(AtLevel(Monkey(), TopLevel(), self.position))

    def _set_add_list(self):
        """
        * El mono tendrá el plátano
        """
        self.add_list.add(Has(Monkey(), Banana()))

    def _set_remove_list(self):
        """ (No se elimina ninguna propiedad) """
        self.remove_list.clear()
