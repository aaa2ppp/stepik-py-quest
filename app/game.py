from enum import IntEnum, Enum
from typing import Optional, List

from util.session import SessionContext


class Direction(IntEnum):
    TOP = 0
    RIGHT = 1
    BOTTOM = 2
    LEFT = 3


class Place:
    def __init__(self, where: str, description: Optional[str] = ""):
        self._where = where
        self._description = description
        self._directions: List[Optional['Place']] = [None] * 4

    @property
    def where(self):
        return self._where

    @property
    def description(self):
        return self._description

    def set_direction(self, direction: Direction, place: Optional['Place']):
        if self._directions[direction] is not place:
            old_place = self._directions[direction]

            if old_place is not None:
                self._directions[direction] = None
                old_place.set_direction(Direction((direction + 2) % 4), None)

            self._directions[direction] = place

            if place is not None:
                place.set_direction(Direction((direction + 2) % 4), self)

    def get_direction(self, direction: Direction) -> Optional['Place']:
        return self._directions[direction]


class GameWin(Place):
    pass


class GameLoss(Place):
    pass


def create_test_location():
    place = GameWin("на балконе")
    place.set_direction(Direction.TOP, GameLoss("свалились с балкона"))
    place.set_direction(Direction.RIGHT, GameLoss("свалились с балкона"))
    place.set_direction(Direction.LEFT, GameLoss("свалились с балкона"))
    place.set_direction(Direction.BOTTOM, Place("в холл"))

    place = place.get_direction(Direction.BOTTOM)
    place.set_direction(Direction.LEFT, Place("в спальню"))
    place.set_direction(Direction.RIGHT, Place("на кухню"))
    place.set_direction(Direction.BOTTOM, Place("в коридор"))

    place = place.get_direction(Direction.BOTTOM)
    place.set_direction(Direction.LEFT, Place("в оружейную"))
    place.set_direction(Direction.RIGHT, Place("в подземелье"))

    return place.get_direction(Direction.RIGHT)


class GameMeta(type):
    def __call__(cls, context: SessionContext):
        instance = context.data.get(cls)
        if instance is None:
            context.data[cls] = instance = super(GameMeta, cls).__call__()
        return instance


class Game(metaclass=GameMeta):
    def __init__(self):
        self._current_place = None

    @property
    def current_place(self) -> Place:
        return self._current_place

    def create_new_location(self):
        self._current_place = create_test_location()

    def delete_location(self):
        self._current_place = None

    def go(self, direction: int, distance: int):
        place = self._current_place

        while distance > 0:
            place = place.get_direction(direction)
            if place is None:
                break
            distance -= 1

        if distance == 0:
            self._current_place = place
            return True
        else:
            return False
