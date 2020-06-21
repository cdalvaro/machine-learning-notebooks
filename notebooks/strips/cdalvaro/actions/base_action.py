from abc import abstractmethod
from typing import List, TypeVar, Union

from ..properties import Properties
from ..state import State

Actions = TypeVar('Actions', bound=List['BaseAction'])


class BaseAction:
    verbose: bool = False

    def __init__(self, name: str, weight: int = 0):
        """
        Clase base para modelizar una acción que aplica sobre un estado.

        Args:
            name (str): Nombre que describe la acción.
            weight (int, optional): El peso que tiene asociada la acción. Default: 0.
        """
        self.name: str = name
        self.weight: int = weight
        self.precondition: Properties = set()
        self.add_list: Properties = set()
        self.remove_list: Properties = set()

    def can_apply(self, state: State, reverse: bool) -> bool:
        """
        Método para comprobar si la acción se puede aplicar sobre el estado indicado.

        Comprueba que las propiedades de precondición de la acción se encuentren
        entre las propiedas del estado indicado.

        Puede aplicarse en el sentido inverso con `reverse=True` para comprobar
        si la acción puede revertirse desde el estado proporcionado.

        Args:
            state (State): Estado sobre el que se quiere comprobar la viabilidad de la acción.
            reverse (bool): Determina si la comprobación es en sentido de aplicar o revertir.

        Returns:
            bool: True si la acción se puede aplicar sobre el estado, o False en caso contario.
        """
        if reverse:
            # Comprueba que alguna de las propiedades que añade la acción
            # esté entre las propiedades del estado a conseguir.
            return len(self.add_list.intersection(state.properties)) > 0

        # Todas las precondiciones de la acción deben estar contenidas
        # en las propiedades del estado sobre el que se aplicaría la acción.
        return self.precondition.intersection(state.properties) == self.precondition

    def apply(self, state: State, reverse: bool = False) -> Union[State, None]:
        """
        Devuelve un nuevo estado a patir de aplicar sobre el estado indicado la acción.

        También puede usarse para generar el pseudo-estado a partir del cuál
        aplicando la acción se puede generar el estado indicado.

        Args:
            state (State): El estado sobre el que se aplica la acción.
            reverse (bool, optional): Revierte la acción aplicada sobre el estado dado.

        Returns:
            State: El estado resultante de aplicar la acción sobre el estado de partida.
        """
        if not self.can_apply(state, reverse):
            return None

        if BaseAction.verbose and not reverse:
            print(f"Aplicando: {self} sobre el estado {state}")

        if reverse:
            # Añade las propiedades de precondición y las que serían eliminadas
            # en caso de aplicarse la acción en sentido normal y se eliminan
            # las propiedades que añadiría la acción.
            properties = state.properties.union(self.remove_list | self.precondition)
            properties = properties.difference(self.add_list)
        else:
            # Se añaden las propiedades de la lista de añadir
            # y se eliminan las propiedades de la lista de eliminar.
            properties = state.properties.union(self.add_list)
            properties = properties.difference(self.remove_list)

        return State(properties)

    @abstractmethod
    def _set_precondition(self):
        """
        Método privado abstracto para establecer las propiedades de precondición.

        Cada clase hija de esta clase debe implementarlo.
        """
        raise NotImplementedError

    @abstractmethod
    def _set_add_list(self):
        """
        Método privado abstracto para establecer las propiedades que se añadirán trás ejecutar la acción.

        Cada clase hija de esta clase debe implementarlo.
        """
        raise NotImplementedError

    @abstractmethod
    def _set_remove_list(self):
        """
        Método privado abstracto para establecer las propiedades que se eliminarán trás ejecutar la acción.

        Cada clase hija de esta clase debe implementarlo.
        """
        raise NotImplementedError

    def __str__(self) -> str:
        return self.name

    def __repr__(self) -> str:
        return self.__str__()

    def __eq__(self, other) -> bool:
        return self.name == other.name

    def __hash__(self) -> int:
        return hash(self.name)
