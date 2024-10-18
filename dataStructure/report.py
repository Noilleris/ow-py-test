class Report:
    report_id: int
    name: str
    credit_score: int

    def __init__(self, report_id: int, name: str, credit_cost: int):
        self.report_id = report_id
        self.name = name
        self.credit_cost = credit_cost