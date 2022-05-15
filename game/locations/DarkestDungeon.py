from util.singleton import SingletonMeta
from game.objects import Location, Place, GameWin, GameLoss, Direction


class DarkestDungeon(Location, metaclass=SingletonMeta):
    name = "Из подземелья на балкон"
    description = "Вы находитесь в темном подземелье. В конце своего путешествия вы должны оказаться на балконе."

    class FallFromWindow(GameLoss):
        _name = "окно"
        _where = "выпали из окна"
        # TODO: need multiline
        _description = "Я знал одну женщину, она всегда выходила в окно." + \
                       " В доме было десять тысяч дверей, но она выходила в окно..."

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
                        Direction.FORWARD: self.FallFromWindow(),
                        Direction.LEFT: finish,
                        Direction.RIGHT: self.FallFromWindow(),
                    }
                ),
                Direction.LEFT: Place(
                    name="спальня", where="в спальне",
                    links={
                        Direction.LEFT: self.FallFromWindow(),
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
