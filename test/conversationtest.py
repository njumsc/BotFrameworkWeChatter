import unittest
import conversation
import time
from user import User


class ConversationTest(unittest.TestCase):
    def setUp(self):
        self.conversation_map = conversation.ConversationMap()
        self.user = User("123", "123")

    def test_update(self):
        self.assertLessEqual(self.conversation_map.update(self.user).last_used_time - time.time(), 10)


if __name__ == '__main__':
    unittest.main()
