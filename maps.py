import json

import data


DATAFILE = "mapdata.json"


def load_json(filename: str) -> dict:
    with open(filename, "r") as f:
        data = json.load(f)
    return data


mapdata = load_json(DATAFILE)
available = list(mapdata.keys())


class Map:
    """Encapsulates a set of connected rooms.

    Attributes
    ----------
    None

    Methods
    -------
    room_names() -> list[str]
    get_room(name: str) -> Room
    locate_char(name: str) -> Room
    """
    def __init__(self, roomdata: dict[str, list[str]]):
        self._rooms = {}
        for name, paths in roomdata.items():
            self._rooms[name] = data.Room(name, paths, False, False)

    def room_names(self) -> list[str]:
        return list(self._rooms)

    def get_room(self, name: str) -> data.Room:
        assert name in self._rooms
        return self._rooms[name]

    def locate_char(self, name: str) -> data.Room:
        for room in self._rooms.values():
            if room.has_char(name):
                return room


def make_map(name: str) -> Map:
    """
    Function takes in the name of the map as input by
    the user.
    It then returns the dictionary of room objects for
    the map if the map name is valid, else it returns -1
    """
    mapdata = load_json(DATAFILE)
    if name.lower() in mapdata:
        return Map(mapdata[name.lower()])
    raise ValueError(f"{name}: no such map")

