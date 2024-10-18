from typing import Optional

from dataStructure.report import Report
from helpers.api import report
from helpers.calculator import CostCalculator


class UsageEntry:
    message_id: int
    text: str
    timestamp: str
    report_id: Optional[str]
    report_name: Optional[str]
    credits_used: float

    def __init__(self, message_id: int, text: str, timestamp: str, report_id: Optional[str] = None):
        self.message_id = message_id
        self.text = text
        self.timestamp = timestamp
        self.report_id = report_id
        self.report_name = None
        self.credits_used = 0

        if report_id is not None:
            raw_report = report(str(report_id))
            if raw_report is not None:
                r = Report(**raw_report)
                self.report_name = r.name
                self.credits_used = r.credit_cost
            else:
                self.credits_used = self.calculate_usage()
        else:
            self.credits_used = self.calculate_usage()

    def calculate_usage(self):
        calculator = CostCalculator(self.text)
        return calculator.calculate_score()

    def to_dict(self):
        return {
            'message_id': self.message_id,
            'timestamp': self.timestamp,
            'report_name': self.report_name,
            'credits_used': self.credits_used,
        }
