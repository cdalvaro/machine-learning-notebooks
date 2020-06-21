from typing import List

from .actions import BaseAction, Actions, GetBanana, MoveHorizontally, ChangeLevel, PushBox
from .element import Banana, Monkey
from .properties import BaseProperty, Properties, AtPosition, TopLevel, GroundLevel
from .state import State


class Heuristic:

    def __init__(self, initial_state: State):
        """
        Clase con la heurística para determinar las posibles acciones
        a aplicar y el orden en el que hacerlo.

        Args:
             initial_state (State): Estado de partida del problema.
        """
        self.initial_state = initial_state

    @staticmethod
    def possible_actions(state: State) -> Actions:
        """
        Método para calcular las posibles acciones a partir de un estado.

        Args:
            state (State): El estado de partida.

        Returns:
            Actions: Las acciones que se pueden tomar desde el estado.
        """
        actions = list()
        positions = [1, 2, 3]

        # Se generan todas las combinaciones posibles de movimiento del mono y de empujar la caja.
        for _from in positions:
            for _to in positions:
                if _from != _to:
                    actions.append(MoveHorizontally(Monkey(), _from, _to))
                    actions.append(PushBox(_from, _to))

        # Se generan todas las combinaciones posibles para que el mono suba y baje de la caja.
        levels = [TopLevel(), GroundLevel()]
        for _from in positions:
            for level in levels:
                actions.append(ChangeLevel(_from, level))

        # Añade la acción que lleva a conseguir el plátano en función de la ubicación de éste.
        for prop in state.properties:
            if type(prop) == AtPosition and prop.element == Banana():
                actions.append(GetBanana(prop.position))

        return actions

    def choose_actions(self, state: State, goal: State) -> Actions:
        """
        Método para elegir en orden de preferencia las posibles acciones que
        llevan desde un estado de partida a un estado objetivo.

        Primero genera todas las posibles acciones de movimiento:
          - Moverse horizontalmente.
          - Moverse verticalmente.
          - Subir/Bajar de la caja.
          - La acción que permite conseguir el plátano en función de la posición de éste.

        Después se seleccionan aquellas acciones que en su lista de añadir
        tengan al menos una propiedad del estado objetivo.

        Args:
            state (State): El estado de partida.
            goal (State): El estado objetivo.

        Returns:
            Actions: la lista de acciones a realizar.
        """
        actions = self.possible_actions(state)

        # Se descartan aquellas acciones que no puedan generar el estado objetivo
        actions = list(set(filter(lambda ac: len(ac.add_list.intersection(goal.properties)) > 0,
                                  actions)))

        # Se ordenan las acciones de mayor a menor peso.
        actions.sort(
            key=lambda ac: (
                # Peso de las propiedades de la acción.
                #   Se calcula como la suma de los pesos de las propiedades del pseudo-estado previo a aplicar
                #   la acción que se está evaluando y que intersectan con las propiedades del estado inicial.
                self._properties_weight(ac, goal),

                # Para resolver 'empates' entre propiedades se tiene en cuenta en segundo lugar el peso de la acción.
                ac.weight
            ), reverse=True)

        return actions

    @staticmethod
    def sort_properties(properties: Properties) -> List[BaseProperty]:
        """
        Método estático para ordenar un conjunto de propiedades por sus pesos.

        Args:
            properties (Properties): El conjunto de propiedades a ordenar.

        Returns:
            List[BaseProperty]: Lista de propiedades ordenadas por pesos de menor a mayor.
        """
        properties = list(properties)
        properties.sort(key=lambda prop: prop.weight)

        return properties

    def _properties_weight(self, action: BaseAction, goal: State) -> int:
        """
        Método privado para calcular el peso total de las propiedades del pseudo-estado
        que aplicándole la acción indicada genera el estado proporcionado.

        Args:
            action (BaseAction): La acción que debe generar el estado `goal`
            goal (State): El estado que genera la acción al aplicarse sobre el pseudo-estado calculado.

        Returns:
            int: La suma de los pesos de las propiedades del pseudo-estado calculado
                 que intersectan con las propiedades del estado inicial del problema.
        """
        prev_state = action.apply(goal, reverse=True)
        if prev_state is None:
            return 0

        properties = prev_state.properties.intersection(self.initial_state.properties)
        return sum(list(map(lambda prop: prop.weight, properties)))
