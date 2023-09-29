


class Room:
    """
    The Room class for each room

    Attributes:
    name: Name of room
    paths: List of rooms that this room has paths connected to
    creature: A boolean for creature presence
    orb: A boolean for powerup presence

    Methods:
    - get_name
    - get_paths
    - has_creature
    - has_orb
    - set_paths
    - set_creature
    - set_orb
    """

    def __init__(self, name: str, paths: list, creature: bool, orb: bool):
        self.name = name
        self.paths = paths
        self.creature = creature
        self.orb = orb

    def get_name(self) -> str:
        """Returns name of room"""
        return self.name

    def get_paths(self) -> list:
        """Return list of paths for the room"""
        return self.paths

    def has_creature(self) -> bool:
        """Returns creature presence in room"""
        return self.creature

    def has_orb(self) -> bool:
        """Returns orb presence in room"""
        return self.orb

    def set_paths(self, paths: list):
        """
        Allows for modification of the list of paths for the room
        """
        self.paths = paths

    def set_creature(self, creature: bool):
        """
        Allows for modification of the presence of a creature
        """
        self.creature = creature

    def set_orb(self, orb: bool):
        """
        Allows for modification of the presence of an orb
        """
        self.orb = orb


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
            self._rooms[name] = Room(name, paths, False, False)

    def room_names(self) -> list[str]:
        return list(self._rooms)

    def get_room(self, name: str) -> Room:
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

