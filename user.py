class User:
    def __init__(self, user, username):
        self.user = user
        self.username = username

    def send(self, text, toUserName = None):
        self.user.send(text, toUserName)