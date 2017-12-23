import time
import config


class ConversationMap:
    conversation_dict = {}

    def __init__(self):
        self.conversation_dict = {}

    def get_conversation(self, username):
        for key in self.conversation_dict.keys():
            if key == username:
                self.update_conversation_dict(key)
                return self.conversation_dict[key]
        return None

    def update(self, user):
        conversation = self.conversation_dict.get(user.username)
        if conversation:
            self.update_conversation_dict(user.username)
            return conversation
        else:
            conversation = Conversation(user, replier())
            new_conversation_dict = {user.username, conversation}
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
        self.sender = sender(username)
        self.conversation_id = sender.start_conversation()
        self.receiver = receiver(username, conversation_id, replier)
        self.last_used_time = time.time()

    def is_overdue(self, now):
        if now - self.last_used_time > config.overdue_time:
            return True
        else:
            return False
