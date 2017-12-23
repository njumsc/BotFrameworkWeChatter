class Replier(object):

    def __init__(self, user):
        self.user = user

    def text(self, text):
        self.user.send(text)