class Replier(object):

    def __init__(self, user):
        self.user = user

    def text(self, text):
        self.user.send_msg(text)

    def pic(self, picFilePath):
        self.user.send_img(picFilePath)
