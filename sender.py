import requests, config

class Sender:

    def __init__(self, conversation_id, userid):
            self.conversation_id = conversation_id
            self.userid = userid

    def send_txt(self, text):
        msg_text = text
        url = 'https://directline.botframework.com/v3/directline/conversations/' + self.userid + '/activities'
        data = {
                "type": "message",
                "from": {
                    "id": self.userid
                },
                "text": msg_text
        }
        requests.post(url, data).json()

   # def send_picture(self, msg):
     #   itchat.send(msg, self.conversation_id)


def start_conversation():
    url = 'https://directline.botframework.com/v3/directline/conversation'
    data = {
        'Authorization': "Bearer " + config.bot_secret_key
    }
    a = requests.post(url,data).json()
    return a["conversationId"]
