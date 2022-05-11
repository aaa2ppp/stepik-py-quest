import bs4
import flask
import htmlmin
from functools import wraps

from flask import request, url_for, redirect

from app import render_template
from game import Game
from util.session import SessionService, SessionContext


def required_session(f):
    """
    Decorator to create session and giving the session context to wrapped function.

    http://flask.pocoo.org/docs/0.12/patterns/viewdecorators/
    """

    @wraps(f)
    def decorated_function(*args, **kwargs):
        session_service = SessionService()
        if session_service.has_session():
            with session_service.get_session_context() as context:
                return f(context, *args, **kwargs)
        else:
            session_service.create_session()
            return redirect(url_for("check_session", next=request.url))

    return decorated_function


def required_location(f):
    @wraps(f)
    def decorated_function(context, *args, **kwargs):
        if get_game(context).location is None:
            return redirect(url_for("select_game"))
        else:
            return f(context, *args, **kwargs)

    return required_session(decorated_function)


def get_game(context: SessionContext) -> Game:
    game = context.data.get(Game.__class__)
    if game is None:
        context.data[Game.__class__] = game = Game(flask.flash)
    return game


def html_prettify(f):
    """
    https://stackoverflow.com/questions/13587531/minify-html-output-from-flask-application-with-jinja2-templates
    """

    @wraps(f)
    def wrapped(*args, **kwargs):
        soup = bs4.BeautifulSoup(f(*args, **kwargs), 'html.parser')
        return soup.prettify()

    return wrapped


def html_minify(f):
    """
    https://stackoverflow.com/questions/13587531/minify-html-output-from-flask-application-with-jinja2-templates
    """

    @wraps(f)
    def wrapped(*args, **kwargs):
        return htmlmin.minify(f(*args, **kwargs), remove_empty_space=True, remove_comments=True)

    return wrapped


def error(code: int, header: str, message: str):
    return render_template("message.html", title="Ошибка", header=header, message=message), code

