from typing import Set, TypeVar

Properties = TypeVar('Properties', bound=Set['BaseProperty'])


class BaseProperty:

    def __init__(self, description: str, weight: int = 0):
        """
        Clase base para modelizar una propiedad de un estado.

        Args:
            description (str): Atributo privado con la descripción de la propiedad.
            weight (int, optional): El peso que tiene asociada la propiedad. Default: 0.
        """
        self.description: str = description
        self.weight: int = weight

    def __str__(self) -> str:
        return self.description

    def __repr__(self) -> str:
        return self.__str__()

    def __eq__(self, other) -> bool:
        return self.description == other.description

    def __hash__(self) -> int:
        return hash(self.description)
