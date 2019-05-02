
class User:
    def __init__(self, login, password, authenticated):
        self.login = login
        self.password = password
        self.authenticated = authenticated

    def to_json(self):
        return {
            'login': self.login,
            'password': self.password,
            'authenticated': self.authenticated
        }

    def is_active(self):
        return True

    def is_authenticated(self):
        return self.authenticated

    def is_anonymous(self):
        return False

    def get_id(self):
        return self.login


def user_from_json(json):
    return User(json['login'], json['password'], json['authenticated'])


class AuthClient:
    def __init__(self, client):
        self.client = client

    def get_user(self, login):
        user = list(self.client.find({'login': login}))
        if len(user) == 0:
            return None
        else:
            return user_from_json(user[0])

    def register(self, body):
        user = self.get_user(body['login'])
        body['authenticated'] = True
        allowed_to_reg = user is None
        if allowed_to_reg:
            self.client.insert_one(body)
        return allowed_to_reg

    def login(self, login):
        self.client.update_one({'login': login}, {"$set": {'authenticated': True}})

    def logout(self, login):
        self.client.update_one({'login': login}, {"$set": {'authenticated': False}})
