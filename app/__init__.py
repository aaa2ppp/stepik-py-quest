from flask import Flask, render_template

from app.helpers import html_prettify, html_minify

app = Flask(__name__)

app.config["SECRET_KEY"] = b'IYsTEl96IluhtQyZFbVy03B+1nzVENXnnxfloJjR5Mw='

if app.debug:
    app.config["TEMPLATES_AUTO_RELOAD"] = True
    render_template = html_prettify(render_template)

else:
    render_template = html_minify(render_template)


from app import routes
