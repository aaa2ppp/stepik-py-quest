from flask import redirect, request, url_for, flash

from app import app, render_template
from app.forms import GameForm
from app.helpers import required_session, get_game, required_location, error
from game import locations, Game
from util.session import SessionService


@app.route("/check-session")
def check_session():
    if SessionService().has_session():
        return redirect(request.args.get('next', url_for("select_game")))
    else:
        return error(code=403,
                     header="Ошибка создания сеанса",
                     message="Я не могу создать сеанс. Такое может происходить, если в вашем броузере" +
                             " заблокированы куки.")


@app.route("/")
@app.route("/select_game")
def select_game():
    return render_template("select_game.html",
                           title="Привет!",
                           locations=((f"start/{location.__name__}", location) for location in locations))


# динамический маршрут
@app.route("/start/<game_name>")
@required_session
def start_game(contex, game_name):
    for location in locations:
        if location.__name__ == game_name:
            contex.data.clear()
            game = get_game(contex)
            game.location = location()
            return redirect(url_for("next_step"))

    return error(code=404,
                 header=f"Игра {game_name} не найдена.",
                 message="Выберете другую игру на начальной странице.")


@app.route("/restart")
@required_location
def restart_game(context):
    game = get_game(context)
    game.start()
    return render_game(game, GameForm(context))


@app.route("/next_step")
@required_location
def next_step(context):
    game = get_game(context)
    return render_game(game, GameForm(context))


@app.route("/do_step", methods=("GET", "POST",))
@required_location
def do_step(context):
    game = get_game(context)
    form = GameForm(context)

    if form.validate_on_submit():
        game.go(form.direction.data, form.distance.data)
        return redirect(url_for("next_step"))
    else:
        flash("Недопустимый ввод", category="error")
        return render_game(game, form)


def render_game(game: Game, form: GameForm):
    return render_template("game.html",
                           title=game.location.name,
                           game=game,
                           form=form,
                           action=url_for("do_step"))


@app.route("/bye")
def bye():
    return render_template("message.html",
                           title="Пока, пока!",
                           message="Ты это, если что заходи...")


@app.route("/TODO")
def todo():
    return render_template("TODO.html", title="TODO")


@app.route("/rules")
def rules():
    return render_template("rules.html", title="Правила")
