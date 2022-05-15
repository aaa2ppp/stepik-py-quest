from random import randrange
from typing import List

from util.bitarray import makeBitArray, testBit
from game.helpers import count_of
from game.objects import Location, Place, GameWin, GameLoss, Direction


def _get_random_pos(height, width):
    return randrange(0, height), randrange(0, width)


class GrimpenMire(Location):
    name = "Гримпенская трясина"
    description = "Вы находитесь в центре Гримпенской трясины. Прыгая с кочки на кочку, вы должны найти сарай," + \
                  " в котором Степлтон держал собаку Баскервилей."
    image = "images/mire.jpeg"

    class Hillock(Place):
        _name = "кочка"
        _where = "на кочке в центре трясины"
        _image = "images/mire2.jpeg"

    class Bog(GameLoss):
        _name = "трясина"
        _where = "утонули в болоте"
        _description = "Свойства трясины весьма коварны. Трясина по-разному реагирует на попадающие в нее живые и" + \
                       " неживые объекты: не трогает мертвое, но засасывает все живое."
        _image = "images/bog2.jpeg"

    def __init__(self):
        # TODO: these should be configurable
        width = 10
        height = 10

        start = self.Hillock()
        finish = GameWin(name="сарай", where="в сарае Степлтона", image="images/barn_on_mire.jpeg")
        super().__init__(start, finish)

        start_pos = _get_random_pos(height, width)
        finish_pos = _get_random_pos(height, width)
        while finish_pos == start_pos:
            finish_pos = _get_random_pos(height, width)

        self._finish_pos = finish_pos
        self._place_pos = {}

        map_line: List[Place | None] = [None] * width
        random_map = makeBitArray(height * width, random=True)
        i = 0
        for row in range(height):
            prev_map_line = map_line
            map_line = [None] * width

            for col in range(width):
                place_pos = (row, col)

                if place_pos == start_pos:
                    place = start
                elif place_pos == finish_pos:
                    place = finish
                else:
                    place = self.Hillock() if testBit(random_map, i) else self.Bog()

                self._place_pos[place] = (row, col)
                map_line[col] = place

                if col > 0:
                    place.set_link(Direction.LEFT, map_line[col - 1])
                if row > 0:
                    place.set_link(Direction.FORWARD, prev_map_line[col])

                i += 1

    def get_hint(self, place):
        finish_pos = self._finish_pos
        place_pos = self._place_pos[place]
        distance = abs(finish_pos[0] - place_pos[0]) + abs(finish_pos[1] - place_pos[1])
        return f"До цели {count_of(distance, 'шаг', 'шага', 'шагов')}"
