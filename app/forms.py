from wtforms import IntegerField, SubmitField, SelectField
from wtforms.validators import InputRequired, NumberRange
from flask_wtf import FlaskForm

from app.game import Direction


class StartGameForm(FlaskForm):
    submit = SubmitField(label="Начать игру")


class GameForm(FlaskForm):
    direction = SelectField(
        "В какую сторону пойдем?",
        choices=(
            (Direction.TOP.value, "Вперед"),
            (Direction.BOTTOM.value, "Назад"),
            (Direction.RIGHT.value, "Вправо"),
            (Direction.LEFT.value, "Влево")
        ),
        coerce=lambda s: Direction(int(s))
    )
    distance = IntegerField(
        "На сколько шагов?",
        default=1,
        validators=[InputRequired(), NumberRange(min=1, max=3)]
    )
    submit = SubmitField(label="В путь!")
    quit = SubmitField(label="Надоело!")
