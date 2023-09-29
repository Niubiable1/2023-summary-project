import data


class Map:
    """Encapsulates a set of connected rooms.

    Attributes
    ----------
    None

    Methods
    -------
    room_names() -> list[str]
    get_room(name: str) -> Room
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


def make_map(name: str) -> Map:
    """
    Function takes in the name of the map as input by
    the user.
    It then returns the dictionary of room objects for
    the map if the map name is valid, else it returns -1
    """
    if name == 'ascent':
        _roompaths = {
            "T-side spawn": ["A lobby", "B lobby"],
            "A lobby": ["T-side spawn", "A main", "Catwalk"],
            "A main": ["A lobby", "A site"],
            "A site": ["A main", "Garden", "CT-side spawn"],
            "B site": ["CT-side spawn", "Market", "B main"],
            "B main": ["B site", "B lobby"],
            "B lobby": ["T-side spawn", "Tiles", "B main"],
            "Tiles": ["B lobby", "Catwalk", "Garden", "Market"],
            "Catwalk": ["A lobby", "Tiles", "Market", "Garden"],
            "Garden": ["A site", "Market", "Catwalk", "Tiles"],
            "Market":
            ["CT-side spawn", "B site", "Tiles", "Catwalk", "Garden"],
            "CT-side spawn": ["A site", "Market", "B site"]
        }
    elif name == 'haven':
        _roompaths = {
            "T-side spawn": ["A garden", "Grass", "C lobby"],
            "A garden": ["T-side spawn", "Mid window", "A lobby"],
            "A lobby": ["A garden", "A short", "A long"],
            "A long": ["A lobby", "A site"],
            "A short": ["A lobby", "A site"],
            "A site": ["A long", "A short", "A link"],
            "A link": ["A site", "Heaven", "B site", "CT-side spawn"],
            "Heaven": ["A link", "A site"],
            "B site": ["A link", "Mid", "C link"],
            "C link": ["B site", "Garage window", "C site", "CT-side spawn"],
            "C site": ["C link", "C long", "Garage"],
            "C long": ["C site", "C lobby"],
            "Mid": ["Mid window", "B site", "Grass"],
            "Mid window": ["Mid", "A garden"],
            "Grass": ["T-side spawn", "Mid", "Garage"],
            "Garage": ["C site", "Garage window", "Grass"],
            "Garage window": ["Garage", "C link"],
            "C lobby": ["T-side spawn", "C long"],
            "CT-side spawn": ["A link", "C link"]
        }
    elif name == 'bind':
        _roompaths = {
            "T-side spawn": ["T-side cave", "A lobby", "Market"],
            "T-side cave": ["T-side spawn", "A lobby", "Market"],
            "A lobby": ["T-side spawn", "T-side cave", "A short", "Showers"],
            "Market":
            ["A short", "B main", "T-side spawn", "T-side cave", "Fountain"],
            "A short": ["A lobby", "Market"],
            "A tp exit": ["A lobby"],
            "Showers": ["A lobby", "A site"],
            "A site":
            ["Showers", "A short", "B tp exit", "U-hall", "CT-side spawn"],
            "U-hall": ["A site"],
            "Heaven": ["A site", "CT-side spawn"],
            "B hall": ["CT-side spawn", "B site", "B elbow"],
            "B site": ["B hall", "B elbow", "Hookah", "Garden"],
            "B elbow": ["B site", "B hall"],
            "Hookah": ["B main", "B site"],
            "B main": ["Market", "Fountain", "Hookah"],
            "Garden": ["B site", "B long", "A tp exit"],
            "B long": ["Fountain", "Garden", "A tp exit"],
            "Fountain": ["Market", "B main", "B long"],
            "B tp exit": ["B main"],
            "CT-side spawn": ["Heaven", "B hall"]
        }
    else:
        raise ValueError(f"{name}: no such map")

    return Map(_roompaths)

