import itchat
from itchat.content import TEXT, PICTURE
import conversation

@itchat.msg_register(TEXT)
def text_main(msg):
    pass

@itchat.msg_register(PICTURE)
def picture_main(msg):
    pass

def get_conversation(username):
