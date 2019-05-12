from app import db
import json
from app.models import User, Friends, Chat, UsersInChat, Message

models = [User, Friends, Chat, UsersInChat, Message]
names = ['users', 'friends', 'chats', 'user_in_chat', 'messages']


def init_db(js_data):
    db.drop_all()
    db.create_all()
    for model, name in zip(models, names):
        model.init_objects(js_data.get(name, []))


def dump_db(file):
    jso = {name: model.dump_objects()
           for model, name in zip(models, names)}
    json.dump(jso, fp=file, indent=4, sort_keys=True)
