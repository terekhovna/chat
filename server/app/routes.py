import flask
from flask import redirect, url_for, request
from app.forms import LoginForm
from app import app
import requests


@app.route('/login', methods=['POST'])
def login_post():
    f = dict(request.form)
    print(f)
    r = requests.post(url_for('login_check', _external=True),
                      json=dict(request.form))
    if not r:
        return redirect(url_for('index'))
    return redirect(url_for('index_user', user=f.get('username')))


@app.route('/login_check', methods=['POST'])
def login_check():
    js = request.get_json(force=True)
    if js.get('password') == 'admin':
        flask.abort(400)
    return 'OK'


@app.route('/login', methods=['GET'])
def login():
    form = LoginForm(request.form)
    return flask.render_template("login.html", form=form)


@app.route('/register', methods=['GET'])
def register():
    pass


@app.route('/messages', methods=['GET'])
def messages():
    pass


@app.route('/messages/<chat>', methods=['GET', 'POST'])
def messages_chat(chat):
    pass


@app.route('/index', methods=['GET'])
def index():
    return flask.render_template("index.html")


@app.route('/index/<user>', methods=['GET'])
def index_user(user):
    return flask.render_template("index.html", user=user)


@app.route('/', methods=['GET'])
def show_begin():
    user = request.args.get('user')
    if user:
        return redirect(url_for('index_user', user=user))
    else:
        return redirect(url_for('index'))
