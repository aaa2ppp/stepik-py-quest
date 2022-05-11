from game.helpers import count_of
from game.locations import Location, locations
from game.units import *
from game.places import Direction


class LocationRequiredError(Exception):
    pass


class Game:
    def __init__(self, log_func=None):
        self._hero = Unit()
        self._location = None
        self._log_func = log_func

    @property
    def hero(self):
        return self._hero

    @property
    def location(self) -> Location:
        return self._location

    @location.setter
    def location(self, location: Location):
        if location is not self._location:
            self._location = location
            self.start()

    def start(self):
        if self._location is None:
            raise LocationRequiredError()

        self._hero.place = self._location.start
        self._log(f"Start new game on {self._location.__class__.__name__} location", category="debug")

    def is_over(self) -> bool:
        return self._hero.place is None or isinstance(self._hero.place, GameOver)

    def go(self, direction: Direction, distance: int):
        self._log(f"Trying to go {distance} steps to the {direction.name.lower()}", category="debug")

        hero = self._hero
        steps_completed = hero.go(direction, distance)

        if hero.is_loser():
            self._log(f"Пройдя {count_of(steps_completed, 'шаг', 'шага', 'шагов')}, вы {hero.place.where}...",
                      category="fail")

        elif hero.is_winner():
            self._log(f"Пройдя {count_of(steps_completed, 'шаг', 'шага', 'шагов')}, вы успешно закончили свое" +
                      f" путешествие {hero.place.where}.", category="success")

        elif steps_completed == 0:
            self._log("Вы не смогли продвинутся ни на один шаг. В эту сторону прохода нет.", category="warning")

        elif steps_completed < distance:
            self._log(f"Вам удалось пройти только {count_of(steps_completed, 'шаг', 'шага', 'шагов')}" +
                      f" из {distance}. Дальше прохода нет.", category="warning")

        else:
            self._log(f"Вы успешно сделали {count_of(steps_completed, 'шаг', 'шага', 'шагов')}.", category="success")

    def _log(self, message: str, category: str = "message"):
        if self._log_func is not None:
            self._log_func(message, category)
