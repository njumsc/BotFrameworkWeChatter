import itchat
from itchat.content import TEXT, PICTURE
import conversation


def get_conversation(user):
    return conversation.ConversationMap.update(user)

@itchat.msg_register(TEXT)
def text_main(msg):
    conv = get_conversation(msg.user)
    conv.sender.send_text(msg.text)

@itchat.msg_register(PICTURE)
def picture_main(msg):
    pass

itchat.auto_login()
itchat.run()
