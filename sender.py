import requests, json, util, log


class Sender:

    def __init__(self, conversation_id, user_id):
        self.conversation_id = conversation_id
        self.user_id = user_id

    def send_text(self, text):
        url = 'https://directline.botframework.com/v3/directline/conversations/' + self.conversation_id + '/activities'
        data = {
            "type": "message",
            "from": {
                "id": self.user_id
            },
            "text": text
        }
        content = json.dumps(data, ensure_ascii=False).encode("utf-8")
        log.info("往conversationId(%s)发送文本消息：%s" % (self.conversation_id, text))

        res = requests.post(url, data=content, headers=util.auth_header({"Content-Type": "application/json"})).json()

    def send_picture(self, msg):
        msg.download(msg.fileName)


def start_conversation():
    url = 'https://directline.botframework.com/v3/directline/conversations'
    a = requests.post(url, headers=util.auth_header()).json()
    return a["conversationId"]
