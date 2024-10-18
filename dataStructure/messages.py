from typing import List

from dataStructure.message import Message

KEY = "messages"

class Messages:
    message: List[Message]

    def __init__(self, data):
        self.messages = [Message(**entry) for entry in data[KEY]]

    def to_dict(self):
        return {'messages': [m.to_dict() for m in self.messages]}
