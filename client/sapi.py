import requests as r

def req_dec(defv):
    def dec(f):
        def func(*args, **kwargs):
            try:
                return f(*args, **kwargs)
            except:
                return defv
        return func
    return dec


@req_dec(False)
def check_connection(site: str) -> bool:
    g = r.get(f'{site}/api/')
    return g.json()['result'] == 'OK'


@req_dec(False)
def check_login(site: str, username: str, password: str) -> bool:
    g = r.get(f'{site}/api/login/', auth=(username, password))
    return bool(g)


@req_dec(False)
def register(site: str, username: str, password: str) -> bool:
    json = {'username': username,
            'password': password}
    g = r.post(f'{site}/api/register/', json=json)
    return bool(g)


@req_dec([])
def get_friends(site: str, username: str, password: str) -> iter:
    g = r.get(f'{site}/api/friend/', auth=(username, password))
    friends = g.json().get('friends', [])
    return (friend['username'] for friend in friends)


@req_dec(False)
def add_friend(site: str, username: str, password: str, friend_name: str) -> bool:
    json = {'friend_name': friend_name}
    g = r.post(f'{site}/api/friend/', auth=(username, password), json=json)
    return bool(g)


@req_dec(False)
def delete_friend(site: str, username: str, password: str, friend_name: str) -> bool:
    json = {'friend_name': friend_name}
    g = r.delete(f'{site}/api/friend/', auth=(username, password), json=json)
    return bool(g)


@req_dec([])
def get_chats(site: str, username: str, password: str) -> iter:
    g = r.get(f'{site}/api/chats/', auth=(username, password))
    chats = g.json().get('chats', [])
    return ((chat['id'], chat['title']) for chat in chats)


@req_dec(False)
def create_chat(site: str, username: str, password: str, title: str, members: iter) -> bool:
    json = {'title': title,
            'members': list(members)}
    g = r.post(f'{site}/api/chats/', auth=(username, password), json=json)
    return bool(g)


@req_dec(False)
def delete_chat(site: str, username: str, password: str, chat_id: int) -> bool:
    json = {'id': chat_id}
    g = r.delete(f'{site}/api/chats/', auth=(username, password), json=json)
    return bool(g)


@req_dec([])
def get_messages(site: str, username: str, password: str, chat_id: int) -> iter:
    g = r.get(f'{site}/api/chats/{chat_id}/', auth=(username, password))
    messages = g.json().get('messages', [])
    return reversed(list((message['author'], message['text']) for message in messages))


@req_dec(False)
def post_message(site: str, username: str, password: str, chat_id: int, text: str) -> bool:
    json = {'text': text}
    g = r.post(f'{site}/api/chats/{chat_id}/', auth=(username, password), json=json)
    return bool(g)

