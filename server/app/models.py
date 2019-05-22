from app import db


class JsonSupp:
    columns = []

    def __init__(self, *args):
        if len(args) != len(self.columns):
            raise Exception
        for name, value in zip(self.columns, args):
            setattr(self, name, value)

    @classmethod
    def init_objects(cls, json):
        for js in json:
            obj = cls.from_json(js)
            db.session.add(obj)
            db.session.commit()

    @classmethod
    def dump_objects(cls):
        objects = cls.query.all()
        objects_list = [obj.to_json() for obj in objects]
        return objects_list

    def to_json(self):
        return {atr: getattr(self, atr)
                for atr in self.columns}

    @classmethod
    def from_json(cls, js):
        return cls(*list(js[atr] for atr in cls.columns))


class User(JsonSupp, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True)
    password = db.Column(db.String(40))
    columns = ["id", "username", "password"]

    def get_friends(self):
        return db.session.query(User).\
         filter(Friends.friend_id == User.id).\
         filter(Friends.user_id == self.id).all()

    def have_friend(self, user):
        return Friends.query.\
            filter_by(user_id=self.id).\
            filter_by(friend_id=user.id).count() > 0

    def add_friend(self, user):
        if user.id == self.id:
            return "i can't add self to friend!"
        if self.have_friend(user):
            return "i have that friend yet"
        friend = Friends(self.id, user.id)
        db.session.add(friend)
        db.session.commit()

    def delete_friend(self, user):
        if not self.have_friend(user):
            return "i haven't got that friend"
        Friends.query.filter_by(user_id=self.id).filter_by(friend_id=user.id).delete()
        db.session.commit()

    def get_chats(self):
        return Chat.query.join(UsersInChat).\
            filter(UsersInChat.user_id == self.id).all()

    def get_chat(self, chat_id):
        return Chat.query.join(UsersInChat).\
            filter(UsersInChat.user_id == self.id).\
            filter(Chat.id == chat_id).first()

    def __repr__(self):
        return "<User : {0.id}, {0.username}, {0.password}>".format(self)


class Friends(JsonSupp, db.Model):
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), primary_key=True)
    friend_id = db.Column(db.Integer, db.ForeignKey('user.id'), primary_key=True)
    columns = ["user_id", "friend_id"]


class Chat(JsonSupp, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(40))
    columns = ["id", "title"]

    def have_member(self, user):
        return Chat.query.join(UsersInChat).\
            filter(UsersInChat.user_id == user.id).\
            filter(Chat.id == self.id).count() > 0


class UsersInChat(JsonSupp, db.Model):
    chat_id = db.Column(db.Integer, db.ForeignKey('chat.id'), primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), primary_key=True)
    columns = ["chat_id", "user_id"]


class Message(JsonSupp, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    chat_id = db.Column(db.Integer, db.ForeignKey('chat.id'))
    post_time = db.Column(db.Integer)
    text = db.Column(db.Text)
    author = db.Column(db.String(80))
    columns = ["id", "chat_id", "post_time", "text", "author"]
