import requests, threading, config

class Receiver:
    def __init__(self, username, conversation_id, replier):
        self.conversation_id = conversation_id
        self.replier = replier
        self.username = username
        self.thread = threading.Thread(target=lambda: self.listen(self))
        self.watermark = ""
        self.start_listening()

    def url(self):
        return "https://directline.botframework.com/v3/directline/conversations/%s/activities?watermark=%s" % (self.conversation_id, self.watermark)

    def listen(self):
        while True:
            res = requests.get(self.url(), headers={"Authorization": config.bot_secret_key}).json()
            self.watermark = res["watermark"]
            for activity in res["activities"]:
                if activity["from"]["id"] != self.username:
                    self.replier.text(activity["text"])

    def start_listening(self):
        self.thread.start()
