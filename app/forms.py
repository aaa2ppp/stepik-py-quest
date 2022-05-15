from wtforms import IntegerField, SubmitField, SelectField
from flask_wtf import FlaskForm
from wtforms.validators import InputRequired, NumberRange

from util.session import SessionService
from game import Direction


class GameForm(FlaskForm):
    direction = SelectField(
        "В какую сторону пойдем?",
        choices=(
            (Direction.FORWARD.name, "Вперед"),
            (Direction.RIGHT.name, "Вправо"),
            (Direction.LEFT.name, "Влево"),
            (Direction.BACKWARD.name, "Назад"),
        ),
        default=lambda: _get_default_value(GameForm, 'direction', Direction.FORWARD.name),
        coerce=lambda name: Direction[name]
    )
    distance = IntegerField(
        "На сколько шагов?",
        default=lambda: _get_default_value(GameForm, 'distance', 1),
        validators=(
            InputRequired(),
            NumberRange(min=1, max=100, message="За раз вы можете сделать от 1 до 100 шагов")
        )
    )
    submit = SubmitField(label="В путь!")

    def __init__(self, context):
        super().__init__()
        self._context_data = context.get_dict(self.__class__)

    def validate(self, *args, **kwargs):
        result = super().validate(*args, **kwargs)
        if result:
            data = self._context_data
            data['direction'] = self.direction.data.name
            data['distance'] = self.distance.data
        return result


# TODO: This is a workaround. I don't understand how to pass the session context data
#  to the form fields in __init__ method of form.
def _get_default_value(form_class, field, default):
    data = SessionService().get_session_context().get(form_class)
    if data is not None:
        value = data.get(field)
        if value is not None:
            return value
    return default
