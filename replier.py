class Replier(object):

    def __init__(self, user):
        self.user = user

    def text(self, text):
        self.user.send(text, toUserName=self.user.username)

    def pic(self, picFilePath):
        self.user.send("@img@%s"%picFilePath, toUserName=self.user.username)