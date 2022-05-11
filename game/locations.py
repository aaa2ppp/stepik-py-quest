from game.places import *
from util.singleton import SingletonMeta

locations = []


def _init():
    locations.append(DarkestDungeon)
    locations.append(GrimpenMire)


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


class DarkestDungeon(Location, metaclass=SingletonMeta):
    name = "Из подземелья на балкон"
    description = "Вы находитесь в темном подземелье. В конце своего путешествия вы должны оказаться на балконе."

    class Window(GameLoss):
        _name = "окно"
        _where = "выпали из окна"
        _description = "Я знал одну женщину, она всегда выходила в окно." + \
                       "В доме было десять тысяч дверей, но она выходила в окно..."

    class FallFromBalcony(GameLoss):
        _name = "свобода"
        _where = "упали с балкона"
        _description = "Мда, пьяный воздух свободы сыграл с профессором Плейшнером злую шутку."

    def __init__(self):
        start = Place(name="подземелье", where="в подземелье", description="Здесь темно, сыро и шныряют большие крысы!")

        finish = GameWin(
            name="балкон", where="на балконе",
            links={
                Direction.FORWARD: self.FallFromBalcony(),
                Direction.BACKWARD: self.FallFromBalcony(),
                Direction.RIGHT: self.FallFromBalcony(),
                Direction.LEFT: self.FallFromBalcony()
            }
        )

        Place(
            name="холл", where="в холле",
            links={
                Direction.FORWARD: Place(
                    name="гостиная", where="в гостиной",
                    links={
                        Direction.FORWARD: self.Window(),
                        Direction.LEFT: finish,
                        Direction.RIGHT: self.Window(),
                    }
                ),
                Direction.LEFT: Place(
                    name="спальня", where="в спальне",
                    links={
                        Direction.LEFT: self.Window(),
                    }
                ),
                Direction.RIGHT: Place(name="кухня", where="на кухне"),
                Direction.BACKWARD: GameLoss(
                    name="темная лестница", where="свалились в лестничный пролет",
                    links={
                        Direction.BACKWARD: Place(
                            name="коридор", where="в коридоре",
                            links={
                                Direction.RIGHT: Place(
                                    name="оружейная",
                                    where="в оружейной"),
                                Direction.LEFT: start
                            }
                        )
                    }
                )
            }
        )

        super().__init__(start, finish)


class GrimpenMire(Location, metaclass=SingletonMeta):
    name = "Гримпенская трясина"
    description = "Вы находитесь в центере Гримпенской трясины. Прыгая с кочки на кочку, вы должны найти сарай," + \
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
        finish = GameWin(
            name="сарай", where="в сарае Степлтона", image="images/barn_on_mire.jpeg",
            links={
                Direction.FORWARD: self.Bog(),
                Direction.BACKWARD: self.Bog(),
                Direction.RIGHT: self.Bog(),
                Direction.LEFT: self.Bog()
            })

        start = self.Hillock(links={
            Direction.FORWARD: self.Bog(),
            Direction.BACKWARD: self.Bog(),
            Direction.RIGHT: self.Bog(),
            Direction.LEFT: self.Bog(links={Direction.LEFT: finish})
        })
        super().__init__(start, finish)


_init()
