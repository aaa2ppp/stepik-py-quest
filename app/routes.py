from flask import redirect, request, url_for, flash

from app import app, render_template
from app.forms import StartGameForm, GameForm
from app.game import Game, GameWin, GameLoss
from app.helpers import open_session
from util.session import SessionService


@app.route("/check-session")
def check_session():
    if SessionService().has_session():
        return redirect(request.args.get('next', url_for("home")))
    else:
        code = 403
        title = "Create session error"
        message = "Can't create session. This usually happens if your browser blocks cookies."
        return render_template("message.html", title=title, message=message), code


@app.route("/", methods=("GET", "POST"))
@open_session
def home(context):
    form = StartGameForm()
    if request.method == "POST" and form.validate_on_submit():
        Game(context).create_new_location()
        return redirect(url_for("new_game"))
    else:
        return render_template("index.html", form=form)


@app.route("/new-game")
@open_session
def new_game(context):
    form = GameForm()
    game = Game(context)
    flash(f"Вы находитесь {game.current_place.where}")
    return render_template("game.html", form=form, action=url_for("next_step"))


@app.route("/next-step", methods=("GET", "POST"))
@open_session
def next_step(context):
    form = GameForm()
    game = Game(context)

    if request.method == "POST" and form.validate_on_submit():
        if form.quit.data:
            game.delete_location()
            return redirect(url_for("bye"))

        game.go(form.direction.data, form.distance.data)
        place = game.current_place

        if isinstance(place, GameWin):
            return redirect(url_for("game_over"))
        elif isinstance(place, GameLoss):
            return redirect(url_for("game_over"))
        else:
            return redirect(url_for("next_step"))
    else:
        flash(f"Вы попали {game.current_place.where}")
        return render_template("game.html", form=form, action="")


@app.route("/game-over")
@open_session
def game_over(context):
    form = StartGameForm()
    game = Game(context)
    place = game.current_place

    if isinstance(place, GameWin):
        flash(f"Победа! Вы {place.where}", category="susses")
    elif isinstance(place, GameLoss):
        flash(f"Oops!.. Вы {place.where}", category="error")

    return render_template("index.html", form=form, action=url_for("home"))


@app.route("/bye")
def bye():
    return render_template("message.html", title="Пока, пока!", message="Ты это, если что заходи...")
