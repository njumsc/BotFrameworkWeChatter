import requests, threading, config, urllib.request, time, os, util, log, re
from PIL import Image


class Receiver:
    def __init__(self, username, conversation_id, replier):
        self.conversation_id = conversation_id
        self.replier = replier
        self.username = username
        self.thread = threading.Thread(target=lambda: self.listen())
        self.watermark = None
        self.start_listening()
        self.thread_stop_flag = False

    def url(self):
        return "https://directline.botframework.com/v3/directline/conversations/%s/activities%s" % (self.conversation_id, "?watermark=" + self.watermark if self.watermark else "")

    def listen(self):
        while not self.thread_stop_flag:
            url = self.url()
            res = requests.get(url, headers=util.auth_header()).json()
            self.watermark = res.get("watermark")
            for activity in res["activities"]:
                if activity["from"]["id"] != self.username:
                    self.reply_text(activity["text"])
                    attachments = activity.get("attachments")
                    if attachments:
                        for attachment in attachments:
                            if attachment["contentType"] == "image/png":
                                url = attachment["contentUrl"]
                                self.reply_pic(url)
                            elif attachment["contentType"] == "application/vnd.microsoft.card.hero":
                                self.reply_hero_card(attachment)
                    suggested_actions = activity.get("suggestedActions")
                    if suggested_actions:
                        self.reply_actions(suggested_actions["actions"], "推荐（请输入括号内的字符串）：")
            time.sleep(config.poll_interval)

    def reply_text(self, text):
        img_re = "!\[.*\]\(.*\)"
        s = re.search(img_re, text)
        if s:
            real_addr = s.group(0).split("(")[1]
            real_addr = real_addr[0:len(real_addr)-1]
            prior = text[0:s.start(0)]
            self.replier.text(prior)
            log.info(prior)
            self.reply_pic(real_addr)
            self.reply_text(text[s.end(0):])
        elif text.strip():
            log.info(text)
            self.replier.text(text.strip())


    def reply_hero_card(self, content):
        card = content["content"]
        title_str = util.or_empty(card.get("title"))
        if title_str:
            title_str += '\n\n'
        title_str += util.or_empty(card.get("text"))
        self.replier.text(title_str)
        if card.get("image"):
            for image in card.get("image"):
                self.reply_pic(image["url"])
        if len(card["buttons"]) > 0:
            self.reply_actions(card["buttons"], "以下选项可用（请输入括号内的字符串）：")

    def reply_actions(self, actions, prompt):
        action_str = prompt + '\n'
        for action in actions:
            if action["type"] == 'imBack':
                title = action["title"]
                if title == "Yes":
                    action_str += "· 是（Yes）"
                elif title == "No":
                    action_str += "· 不（No）"
                else:
                    action_str += "· %s（%s）" % (action["title"], action["value"])
                action_str += "\n"
            elif action["type"] == 'openUrl':
                action_str += '· %s(%s)\n' % (action["title"], action["value"])
        self.replier.text(action_str)

    def reply_pic(self, pic_url):
        log.info("接收到图片，地址：" + pic_url)
        filename = "%s_%s" % (time.time(), self.conversation_id)
        pngfile = filename + ".png"
        webpfile = filename + ".webp"
        util.download_file(pic_url, webpfile)
        Image.open(webpfile).convert("RGB").save(pngfile, "png")
        self.replier.pic(pngfile)
        os.remove(pngfile)
        os.remove(webpfile)

    def start_listening(self):
        self.thread.setDaemon(True)
        self.thread.start()
    
    def dispose(self):
        self.thread_stop_flag = True

