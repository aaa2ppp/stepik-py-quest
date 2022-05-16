from flask import redirect, request, url_for, flash, get_flashed_messages

from app import app, render_template
from app.forms import GameForm
from app.helpers import get_game, error, required_session, required_location
from game import locations as game_locations, GameNotFoundError
from util.session import SessionService


@app.route("/check-session")
def check_session():
    if SessionService().has_session():
        return redirect(request.args.get('next', url_for("select_game")))
    else:
        return error(code=401,
                     header="Ошибка создания сеанса",
                     message="Я не могу создать сеанс. Такое может происходить, если в вашем браузере" +
                             " заблокированы куки.")


@app.route("/")
def select_game():
    return render_template(
        "select_game.html",
        title="Привет!",
        game_locations=game_locations,
    )


# динамический маршрут
@app.route("/start/<game_name>")
@required_session
def start_game(contex, game_name):
    get_flashed_messages()  # clear log
    contex.data.clear()

    try:
        game = get_game(contex)
        game.start(game_name)
    except GameNotFoundError:
        return error(code=404,
                     header=f"Игра {game_name} не найдена.",
                     message="Выберите другую игру на начальной странице.")

    return redirect(url_for("next_step"))


@app.route("/restart")
@required_location
def restart_game(context):
    game = get_game(context)
    game.start()
    return redirect(url_for("next_step"))


@app.route("/next_step", methods=("GET", "POST",))
@required_location
def next_step(context):
    game = get_game(context)
    form = GameForm(context)
    code = 200

    if form.is_submitted():

        if form.validate():
            game.go(form.direction.data, form.distance.data)
            return redirect(url_for("next_step"))
        else:
            code = 422
            flash("Недопустимый ввод", category="error")

    return (render_template("game.html",
                            title=game.location.name,
                            game=game,
                            form=form),
            code)


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
