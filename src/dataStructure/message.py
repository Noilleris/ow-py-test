from typing import Optional
KEY = "messages"

class Message:
    text: str
    timestamp: str
    report_id: Optional[int]
    id: int

    def __init__(self, id: int, text: str, timestamp: str, report_id: Optional[int] = None):
        self.id = id
        self.text = text
        self.timestamp = timestamp
        self.report_id = report_id

    def to_dict(self):
        return {
            'id': self.id,
            'timestamp': self.timestamp,
            'text': self.text,
            'report_id': self.report_id,
        }

