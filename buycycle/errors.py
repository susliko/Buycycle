class AlreadyRegisteredError(Exception):
    def __init__(self, status='registration_error', message='user already registered'):
        self.message = message
        self.status = status


class LoginFailedError(Exception):
    def __init__(self, status='login_error', message='invalid username or password'):
        self.message = message
        self.status = status


class AccessDeniedError(Exception):
    def __init__(self, status='access_error', message='this user is not allowed to access requested data'):
        self.message = message
        self.status = status
