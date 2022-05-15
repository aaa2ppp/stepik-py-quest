from enum import IntEnum
from typing import Optional, List, Dict


class Direction(IntEnum):
    FORWARD = 0
    RIGHT = 1
    BACKWARD = 2
    LEFT = 3


class Place:
    _name = "какое-то место"
    _where = "в каком-то месте"
    _description = None
    _image = None

    def __init__(self,
                 name: Optional[str] = None,
                 where: Optional[str] = None,
                 description: Optional[str] = None,
                 image: Optional[str] = None,
                 links: Optional[Dict[Direction, 'Place']] = None
                 ):
        if name is not None:
            self._name = name

        if where is not None:
            self._where = where

        if description is not None:
            self._description = description

        if image is not None:
            self._image = image

        self._links: List[Optional['Place']] = [None] * 4
        if links is not None:
            self.set_links(links)

    @property
    def name(self):
        return self._name

    @property
    def where(self):
        return self._where

    @property
    def description(self):
        return self._description

    @property
    def image(self):
        return self._image

    @property
    def forward(self):
        return self._links[Direction.FORWARD]

    @property
    def backward(self):
        return self._links[Direction.BACKWARD]

    @property
    def right(self):
        return self._links[Direction.RIGHT]

    @property
    def left(self):
        return self._links[Direction.LEFT]

    def get_link(self, direction: Direction) -> Optional['Place']:
        return self._links[direction]

    def set_link(self, direction: Direction, place: Optional['Place']):
        old_place = self._links[direction]

        if old_place is place:
            return

        if old_place is not None:
            self._links[direction] = None
            old_place.set_link(Direction((direction + 2) % 4), None)

        self._links[direction] = place

        if place is not None:
            place.set_link(Direction((direction + 2) % 4), self)

    def set_links(self, links: Dict[Direction, Optional['Place']]):
        for direction, place in links.items():
            self.set_link(direction, place)


class GameOver(Place):
    pass


class GameWin(GameOver):
    _name = "победа"


class GameLoss(GameOver):
    _name = "поражение"


class Location:
    name = "location"
    description = None
    image = None

    def __init__(self, start: Place, finish: Place):
        self._start = start
        self._finish = finish

    @property
    def start(self) -> Place:
        return self._start

    @property
    def finish(self) -> Place:
        return self._finish

    def get_hint(self, place):
        return None


class Unit:
    def __init__(self):
        self._place = None

    @property
    def place(self) -> Place:
        return self._place

    @place.setter
    def place(self, place: Place):
        self._place = place

    def go(self, direction: Direction, distance: int) -> int:
        if self._place is None or isinstance(self._place, GameOver):
            return 0

        count = 0
        for _ in range(distance):
            new_place = self._place.get_link(direction)
            if new_place is None:
                break
            self._place = new_place
            count += 1
        return count

    def is_winner(self) -> bool:
        return isinstance(self._place, GameWin)

    def is_loser(self) -> bool:
        return isinstance(self._place, GameLoss)
