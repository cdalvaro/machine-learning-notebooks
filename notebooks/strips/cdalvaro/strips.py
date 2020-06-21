from typing import Union
from random import shuffle

from .actions import BaseAction, Actions
from .heuristic import Heuristic
from .state import State


class Strips:
    # Límite de iteraciones en el que se tendrá en cuenta el orden
    # establecido por la heurística en la búsqueda de acciones.
    efficiency_limit: int = 10

    def __init__(self, initial_state: State, goal: State, heuristic: Heuristic):
        """
        Clase que implementa la generación de planes de acción basada en STRIPS.

        Args:
            initial_state (State): Estado inicial del que parte el problema.
            goal (State): Estado objetivo que debe alcanzar la planificación.
            heuristic (Heuristic): Instancia de heurística para determinar las acciones del plan.
        """
        self.initial_state: State = initial_state
        self.goal: State = goal
        self.heuristic: Heuristic = heuristic

    def get_plan(self) -> Union[Actions, bool]:
        """
        Método que implementa la lógica para la búsqueda del plan.

        Returns:
            Union[Actions, bool]: Devuelve el conjunto de acciones ordenadas que
            componen el plan o False indicando que no ha sido posible elaborar un plan.
        """
        plan: Actions = list()

        state = self.initial_state
        targets = list(self.goal.properties)

        iteration_counter = 0
        show_warning = True

        while len(targets) > 0:
            iteration_counter += 1

            # Se extrae el primer objetivo de la lista de objetivos.
            target = targets.pop(0)

            # Si el objetivo a explorar se trata de una acción:
            # - Se aplica la acción sobre el estado actual y si se puede generar un
            #   nuevo estado válido se actualiza el estado actual y se añade la acción al plan.
            if issubclass(type(target), BaseAction):
                new_state = target.apply(state)
                if new_state is not None:
                    state = new_state
                    plan.append(target)

            # Si no es una acción, entonces es una propiedad.
            else:

                # Si el objetivo es una propiedad del estado actual:
                # - No se hace nada y se explora el siguiente objetivo de la lista.
                if target in state.properties:
                    continue

                # Se generan las posibles acciones que pueden dar lugar desde el estado
                # actual un estado que tiene como propiedad el objetivo que se está estudiando.
                actions = self.heuristic.choose_actions(state, State({target}))
                if len(actions) == 0:
                    # Si no hay acciones posibles, no se ha conseguido elaborar
                    # la planificación y se devuelve False
                    return False

                if iteration_counter > self.efficiency_limit:
                    # Se anula el orden calculado por la heurística si el número
                    # de iteraciones es alto para evitar bucles infinitos
                    if show_warning:
                        print("AVISO: La heurística no está encontrando soluciones eficientes")
                        show_warning = False
                    shuffle(actions)

                # Se añade la primera acción devuelta por la heurística a la lista de objetivos.
                action = actions.pop(0)
                targets.insert(0, action)

                # Además de añadir la acción, se anteponen sus precondiciones
                # para buscar las acciones que generen estas precondiciones.
                targets = self.heuristic.sort_properties(action.precondition) + targets

        return plan
