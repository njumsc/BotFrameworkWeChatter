
class User:
    def __init__(self, user, username):
        self.user = user
        self.username = username

    def send_msg(self, text):
        self.user.send_msg(text)

    def send_img(self, path):
        self.user.send_image(path)
