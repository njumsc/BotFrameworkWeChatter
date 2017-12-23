import time
import config
from replier import Replier
from sender import Sender, start_conversation
from receiver import Receiver


class ConversationMap:
    conversation_dict = {}

    def __init__(self):
        self.conversation_dict = {}

    def update(self, user):
        conversation = self.conversation_dict.get(user.username)
        if conversation:
            self.update_conversation_dict(user.username)
            return conversation
        else:
            conversation = Conversation(user, Replier(user))
            new_conversation_dict = {user.username: conversation}
            self.conversation_dict.update(new_conversation_dict)
            return conversation

    def delete_overdue(self):
        for key in self.conversation_dict.keys():
            if self.conversation_dict[key].is_overdue():
                self.conversation_dict.pop(key)
            else:
                return

    def update_conversation_dict(self, key):
        self.conversation_dict[key].last_used_time = time.time()
        sorted(self.conversation_dict.items(), key=lambda d: d[1].last_used_time)


class Conversation:
    def __init__(self, user, replier):
        self.user = user
        self.conversation_id = start_conversation()
        self.sender = Sender(self.conversation_id, user.username)
        self.receiver = Receiver(user.username, self.conversation_id, replier)
        self.last_used_time = time.time()

    def is_overdue(self, now):
        return now - self.last_used_time > config.overdue_time
