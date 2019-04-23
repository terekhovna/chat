from flask import jsonify, make_response
from flask_httpauth import HTTPBasicAuth
from app.models import User

auth = HTTPBasicAuth()


@auth.error_handler
def unauthorized():
    return make_response(jsonify({'error': 'authentication error'}), 403)


@auth.get_password
def get_password(username):
    user = User.query.filter_by(username=username).first()
    if user:
        return user.password
    return None
