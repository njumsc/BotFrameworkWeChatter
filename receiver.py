import requests, threading, config, urllib.request, time, os, util
from PIL import Image

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
                                url = attachment["contentUrl"]
                                self.reply_pic(url)
                            elif attachment["contentType"] == "application/vnd.microsoft.card.hero":
                                self.reply_hero_card(attachment)
            time.sleep(config.poll_interval)

    def reply_hero_card(self, content):
        card = content["content"]
        self.replier.text("%s\n\n%s" % (card["title"], card["text"]))
        for image in card["images"]:
            self.reply_pic(image["url"])
        if len(card["buttons"]) > 0:
            action = '以下选项可用：\n\n'
            for button in card["buttons"]:
                if button["type"] == 'imBack':
                    title = button["title"]
                    if title == "Yes":
                        action += "· 是"
                    elif title == "No":
                        action += "· 不"
                    else:
                        action += "· " + title
                    action += "\n\n"
                elif button["type"] == 'openUrl':
                    action += '· %s(%s)\n\n' % (button["title"], button["value"])
            self.replier.text(action)


    def reply_pic(self, pic_url):
        filename = "%s_%s" % (time.time(), self.conversation_id)
        pngfile = filename + ".png"
        webpfile = filename + ".webp"
        urllib.request.urlretrieve(pic_url, webpfile)
        Image.open(webpfile).convert("RGB").save(pngfile, "png")
        self.replier.pic(pngfile)
        os.remove(pngfile)
        os.remove(webpfile)




    def start_listening(self):
        self.thread.setDaemon(True)
        self.thread.start()

