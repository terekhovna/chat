from app import app, db
from flask import jsonify, request
from app.models import User, Friends, Chat, UsersInChat, Message
from flask_httpauth import HTTPBasicAuth
from flask import make_response
from app.authentic import auth
from sqlalchemy import func


def get_user(**kwargs):
    user = User.query.filter_by(**kwargs).first()
    return user


def register_user(user_id, username, password):
    if get_user(id=user_id):
        return 'i have user with same id'

    if get_user(username=username):
        return 'i have user with same username'

    user = User(user_id, username, password)
    db.session.add(user)
    db.session.commit()


def get_max_id(cls):
    res = db.session.query(func.max(cls.id)).scalar()
    return res or 0


def to_json(object_list):
    return list(map(lambda x: x.to_json(), object_list))


def create_chat(admin, members, chat_id, title):
    members = [get_user(username=mem) for mem in members]
    if not all(admin.have_friend(mem) for mem in members):
        return "one of members is not admin's friend"
    if Chat.query.filter_by(id=chat_id).count() > 0:
        return "i already have chat with this id"

    chat = Chat(chat_id, title)
    db.session.add(chat)
    db.session.commit()

    members.append(admin)
    db.session.add_all([UsersInChat(chat_id, m.id)
                        for m in members])
    db.session.commit()


def get_messages(chat):
    return Message.query.filter_by(chat_id=chat.id).all()


def delete_chat(user, chat_id):
    chat = user.get_chat(chat_id)
    if not chat:
        return "i haven't got chat with this id"
    
    UsersInChat.query.filter_by(chat_id=chat_id).filter_by(user_id=user.id).delete()
    db.session.commit()


def post_message(user, chat_id, text):
    chat = user.get_chat(chat_id)
    if not chat:
        return "i haven't got chat with this id"

    from time import time
    message = Message(get_max_id(Message) + 1, chat_id, int(time()), text, user.username)

    db.session.add(message)
    db.session.commit()
