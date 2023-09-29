"""data.py

This module contains superclasses used by the other modules.

It should not import any other modules.
"""


class Character:
    """
    Base class for characters in the game.

    Attribrute:
    name: str
    hp: int
    """
    name: str
    hp: int


class Object:
    """Base class for objects in the game."""
    name: str


class Room:
    """Encapsulates objects and characters.

    Contains path data to other rooms.

    Attributes
    ----------
    + name: str

    Methods
    -------
    + characters() -> list[str]
    + give_char(name: str) -> Character
    + give_obj(name: str) -> Object
    + has_char(name: str) -> bool
    + has_obj(name: str) -> bool
    + objects() -> list[str]
    + paths() -> list[str]
    + take_char(char: Character) -> None
    + take_obj(obj: Object) -> None
    """
    def __init__(self, name: str, paths: list[str]):
        self.name = name
        self._paths = paths
        self._objects = []
        self._characters = []

    def characters(self) -> list[str]:
        return [char.name for char in self._characters]

    def give_char(self, name: str) -> Character:
        for i, char in enumerate(self._characters):
            if char.name == name:
                return self._characters.pop(i)
        raise ValueError(f"{name}: no such char")

    def give_obj(self, name: str) -> Object:
        for i, obj in enumerate(self._objects):
            if obj.name == name:
                return self._objects.pop(i)
        raise ValueError(f"{name}: no such obj")

    def has_char(self, name: str) -> bool:
        for char in self._characters:
            if char.name == name:
                return True
        return False

    def has_obj(self, name: str) -> bool:
        for obj in self._objects:
            if obj.name == name:
                return True
        return False

    def objects(self) -> list[str]:
        return [obj.name for obj in self._objects]

    def paths(self) -> list[str]:
        return self._paths.copy()
        
    def take_obj(self, obj: Object) -> None:
        self._objects.append(obj)

    def take_char(self, char: Character) -> None:
        self._characters.append(char)


