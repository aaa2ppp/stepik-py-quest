from game.places import *


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
