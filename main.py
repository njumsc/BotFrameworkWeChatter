import itchat
from itchat.content import TEXT, PICTURE
import conversation
from user import User


def get_conversation(msg):
    return conversation.ConversationMap.update(User(msg.user, msg.username))

@itchat.msg_register(TEXT)
def text_main(msg):
    conv = get_conversation(msg)
    conv.sender.send_text(msg.text)

@itchat.msg_register(PICTURE)
def picture_main(msg):
    pass

itchat.auto_login()
itchat.run()
