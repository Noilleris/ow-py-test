from typing import List

from src.dataStructure.message import Message
from src.dataStructure.usageEntry import UsageEntry

class Usage:
    def __init__(self, messages: List[Message]):
        self.usage = [UsageEntry(m.id, m.text, m.timestamp, m.report_id) for m in messages]

    def to_dict(self):
        return {'usage': [entry.to_dict() for entry in self.usage]}
