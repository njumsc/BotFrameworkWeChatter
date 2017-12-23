import requests, config, time, json, util


class Sender:

    def __init__(self, conversation_id, userid):
        self.conversation_id = conversation_id
        self.userid = userid

    def send_text(self, text):
        url = 'https://directline.botframework.com/v3/directline/conversations/' + self.conversation_id + '/activities'
        data = {
            "type": "message",
            "from": {
                "id": self.userid
            },
            "text": text
        }
        content = json.dumps(data,ensure_ascii=False).encode("utf-8")
        print(content)

        res = requests.post(url, data=content, headers=util.auth_header({"Content-Type": "application/json"})).json()
        print(res)




# def send_picture(self, msg):
#   itchat.send(msg, self.conversation_id)


def start_conversation():
    url = 'https://directline.botframework.com/v3/directline/conversations'
    data = {
        'Authorization': "Bearer " + config.bot_secret_key
    }
    a = requests.post(url, headers=data).json()
    return a["conversationId"]
