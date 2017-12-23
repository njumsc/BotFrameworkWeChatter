import requests, threading, config, urllib.request, time, os, util

class Receiver:
    def __init__(self, username, conversation_id, replier):
        self.conversation_id = conversation_id
        self.replier = replier
        self.username = username
        self.thread = threading.Thread(target=lambda: self.listen())
        self.watermark = None
        self.start_listening()

    def url(self):
        return "https://directline.botframework.com/v3/directline/conversations/%s/activities%s" % (self.conversation_id, "?watermark=" + self.watermark if self.watermark else "")

    def listen(self):
        while True:
            url = self.url()
            res = requests.get(url, headers=util.auth_header()).json()
            self.watermark = res.get("watermark")
            for activity in res["activities"]:
                if activity["from"]["id"] != self.username:
                    self.replier.text(activity["text"])
                    attachments = activity.get("attachments")
                    if attachments:
                        for attachment in attachments:
                            if attachment["contentType"] == "image/png":
                                url = content["contentUrl"]
                                filename = "%s_%s" % (time.time(), url)
                                urllib.request.urlretrieve(url, filename)
                                self.replier.pic(url)
                                os.remove(filename)




    def start_listening(self):
        self.thread.setDaemon(True)
        self.thread.start()

