import requests as r


def request_decorator(default_value):
    def decorator(f):
        def func(*args, **kwargs):
            try:
                return f(*args, **kwargs)
            except r.exceptions.ConnectionError:
                return default_value
        return func
    return decorator


@request_decorator(False)
def check_connection(site: str) -> bool:
    request = r.get(f'{site}/api/')
    return request.json()['result'] == 'OK'


@request_decorator(False)
def check_login(site: str, username: str, password: str) -> bool:
    request = r.get(f'{site}/api/login/', auth=(username, password))
    return bool(request)


@request_decorator(False)
def register(site: str, username: str, password: str) -> bool:
    json = {'username': username,
            'password': password}
    request = r.post(f'{site}/api/register/', json=json)
    return bool(request)


@request_decorator([])
def get_friends(site: str, username: str, password: str) -> iter:
    request = r.get(f'{site}/api/friend/', auth=(username, password))
    friends = request.json().get('friends', [])
    return (friend['username'] for friend in friends)


@request_decorator(False)
def add_friend(site: str, username: str, password: str, friend_name: str) -> bool:
    json = {'friend_name': friend_name}
    request = r.post(f'{site}/api/friend/', auth=(username, password), json=json)
    return bool(request)


@request_decorator(False)
def delete_friend(site: str, username: str, password: str, friend_name: str) -> bool:
    json = {'friend_name': friend_name}
    request = r.delete(f'{site}/api/friend/', auth=(username, password), json=json)
    return bool(request)


@request_decorator([])
def get_chats(site: str, username: str, password: str) -> iter:
    request = r.get(f'{site}/api/chats/', auth=(username, password))
    chats = request.json().get('chats', [])
    return ((chat['id'], chat['title']) for chat in chats)


@request_decorator(False)
def create_chat(site: str, username: str, password: str, title: str, members: iter) -> bool:
    json = {'title': title,
            'members': list(members)}
    request = r.post(f'{site}/api/chats/', auth=(username, password), json=json)
    return bool(request)


@request_decorator(False)
def delete_chat(site: str, username: str, password: str, chat_id: int) -> bool:
    json = {'id': chat_id}
    request = r.delete(f'{site}/api/chats/', auth=(username, password), json=json)
    return bool(request)


@request_decorator([])
def get_messages(site: str, username: str, password: str, chat_id: int) -> iter:
    request = r.get(f'{site}/api/chats/{chat_id}/', auth=(username, password))
    messages = request.json().get('messages', [])
    return reversed(list((message['author'], message['text']) for message in messages))


@request_decorator(False)
def post_message(site: str, username: str, password: str, chat_id: int, text: str) -> bool:
    json = {'text': text}
    request = r.post(f'{site}/api/chats/{chat_id}/', auth=(username, password), json=json)
    return bool(request)

