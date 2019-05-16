from app import app
from flask import jsonify, request
from app.models import User, Chat
from flask import make_response
from werkzeug import exceptions
from app.authentic import auth
from app.api_logic import get_user, get_max_id, register_user,\
    to_json, create_chat, delete_chat, post_message, get_messages


def get_json():
    try:
        js = request.get_json(force=True)
    except exceptions.BadRequest:
        return None
    if not isinstance(js, dict):
        return None
    return js


def return_error(s: str = ""):
    return make_response(jsonify({'error': s}), 403)


def return_ok():
    return make_response(jsonify({'result': 'OK'}), 200)


@app.route('/api/', methods=['GET'])
def check_connection():
    return return_ok()


@app.route('/api/login/', methods=['GET'])
@auth.login_required
def api_login():
    user = get_user(username=auth.username())
    return jsonify(user.to_json())


@app.route('/api/register/', methods=['POST'])
def api_register():
    js = get_json()

    if not js:
        return return_error('corrupted json')

    if not js.get('username'):
        return return_error('i need username')

    if not js.get('password'):
        js['password'] = js['username']

    if not js.get('id'):
        js['id'] = get_max_id(User) + 1

    re = register_user(js['id'], js['username'], js['password'])
    if re:
        return return_error(re)
    else:
        return return_ok()


@app.route('/api/friend/', methods=['GET'])
@auth.login_required
def api_friend_get():
    user = get_user(username=auth.username())
    return jsonify({'friends':
                    to_json(user.get_friends())})


@app.route('/api/friend/', methods=['POST'])
@auth.login_required
def api_friend_post():
    js = get_json()

    if not js:
        return return_error('corrupted json')

    if not js.get('friend_name'):
        return return_error('i need friend name')

    user = get_user(username=auth.username())
    friend = get_user(username=js['friend_name'])
    if not friend:
        return return_error('wrong friend name')

    re = user.add_friend(friend)
    if re:
        return return_error(re)
    else:
        return return_ok()


@app.route('/api/friend/', methods=['DELETE'])
@auth.login_required
def api_friend_delete():
    js = get_json()

    if not js:
        return return_error('corrupted json')

    if not js.get('friend_name'):
        return return_error('i need friend name')

    user = get_user(username=auth.username())
    friend = get_user(username=js['friend_name'])
    if not friend:
        return return_error('wrong friend name')

    re = user.delete_friend(friend)
    if re:
        return return_error(re)
    else:
        return return_ok()


@app.route('/api/chats/', methods=['GET'])
@auth.login_required
def api_get_chats():
    user = get_user(username=auth.username())
    return jsonify({'chats':
                    to_json(user.get_chats())})


@app.route('/api/chats/', methods=['POST'])
@auth.login_required
def api_create_chat():
    js = get_json()

    if not js:
        return return_error('corrupted json')

    user = get_user(username=auth.username())
    if not js.get('id'):
        js['id'] = get_max_id(Chat) + 1
    if not js.get('title'):
        js['title'] = js['id']
    re = create_chat(user, js.get('members', []), js['id'], js['title'])
    if re:
        return return_error(re)
    else:
        return return_ok()


@app.route('/api/chats/', methods=['DELETE'])
@auth.login_required
def api_delete_chat_for_user():
    js = get_json()

    if not js:
        return return_error('corrupted json')

    user = get_user(username=auth.username())
    if not js.get('id'):
        return return_error("i need id of chat")
    re = delete_chat(user, js['id'])
    if re:
        return return_error(re)
    else:
        return return_ok()


@app.route('/api/chats/<int:chat_id>/', methods=['GET'])
@auth.login_required
def api_get_messages(chat_id):
    user = get_user(username=auth.username())
    chat = user.get_chat(chat_id)
    if not chat:
        return return_error('i have not got that chat')

    return jsonify({'chat': chat.to_json(),
                    'messages': to_json(get_messages(chat))})


@app.route('/api/chats/<int:chat_id>/', methods=['POST'])
@auth.login_required
def api_post_message(chat_id):
    js = get_json()

    if not js:
        return return_error('corrupted json')

    user = get_user(username=auth.username())

    if not js.get('text'):
        return return_error('i need text of message')

    re = post_message(user, chat_id, js['text'])
    if re:
        return return_error(re)
    else:
        return return_ok()
